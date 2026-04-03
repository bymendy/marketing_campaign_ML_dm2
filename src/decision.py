# ============================================================
# Partie G - Optimisation de la decision marketing
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import joblib
import yaml

warnings.filterwarnings('ignore')

# ── Chargement ───────────────────────────────────────────
df_scores = pd.read_csv('data/processed/df_scores.csv')
df_full   = pd.read_csv('data/processed/df_clustered.csv')

# Paramètres business (depuis configs/)
with open('configs/thresholds.yaml', 'r') as f:
    config = yaml.safe_load(f)

COST_CONTACT   = config['cost_contact']    # 10 euros par contact
REVENUE_CONV   = config['revenue_conversion']  # 100 euros par conversion

print("=" * 60)
print("PARTIE G — OPTIMISATION DECISION MARKETING")
print("=" * 60)
print(f"Cout contact    : {COST_CONTACT} euros")
print(f"Revenu conversion : {REVENUE_CONV} euros")
print(f"Clients dans le test set : {len(df_scores)}")
print(f"Repondants reels : {df_scores['y_true'].sum()}")

# ── 1. ANALYSE DU SEUIL DE DECISION ──────────────────────
print("\n" + "=" * 60)
print("1. OPTIMISATION DU SEUIL DE DECISION")
print("=" * 60)

thresholds  = np.arange(0.05, 0.95, 0.01)
profits     = []
n_contacted = []
n_converted = []
precisions  = []
recalls     = []

for threshold in thresholds:
    y_pred_t = (df_scores['y_proba'] >= threshold).astype(int)
    tp = ((y_pred_t == 1) & (df_scores['y_true'] == 1)).sum()
    fp = ((y_pred_t == 1) & (df_scores['y_true'] == 0)).sum()
    fn = ((y_pred_t == 0) & (df_scores['y_true'] == 1)).sum()

    contacted = tp + fp
    profit    = (tp * REVENUE_CONV) - (contacted * COST_CONTACT)
    precision = tp / contacted if contacted > 0 else 0
    recall    = tp / (tp + fn) if (tp + fn) > 0 else 0

    profits.append(profit)
    n_contacted.append(contacted)
    n_converted.append(tp)
    precisions.append(precision)
    recalls.append(recall)

results_df = pd.DataFrame({
    'Threshold':   thresholds,
    'Profit':      profits,
    'Contacted':   n_contacted,
    'Converted':   n_converted,
    'Precision':   precisions,
    'Recall':      recalls
})

# Seuil optimal = profit maximum
best_idx       = results_df['Profit'].idxmax()
best_threshold = results_df.loc[best_idx, 'Threshold']
best_profit    = results_df.loc[best_idx, 'Profit']
best_contacted = results_df.loc[best_idx, 'Contacted']
best_converted = results_df.loc[best_idx, 'Converted']
best_precision = results_df.loc[best_idx, 'Precision']
best_recall    = results_df.loc[best_idx, 'Recall']

print(f"\nSeuil optimal identifie : {best_threshold:.2f}")
print(f"Profit maximum         : {best_profit:.0f} euros")
print(f"Clients contactes      : {best_contacted}")
print(f"Conversions attendues  : {best_converted}")
print(f"Precision              : {best_precision:.2f}")
print(f"Recall                 : {best_recall:.2f}")

# Sauvegarde seuil optimal
config['optimized_threshold'] = float(round(best_threshold, 2))
with open('configs/thresholds.yaml', 'w') as f:
    yaml.dump(config, f)
print(f"\nSeuil optimal sauvegarde -> configs/thresholds.yaml")

# ── 2. VISUALISATION PROFIT vs SEUIL ─────────────────────
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# Profit
axes[0].plot(results_df['Threshold'], results_df['Profit'],
             color='#4f6ef7', linewidth=2)
axes[0].axvline(best_threshold, color='red', linestyle='--',
                label=f'Seuil optimal : {best_threshold:.2f}')
axes[0].axhline(0, color='gray', linestyle=':', linewidth=1)
axes[0].fill_between(results_df['Threshold'], results_df['Profit'],
                     where=results_df['Profit'] > 0,
                     alpha=0.1, color='green', label='Zone profitable')
axes[0].set_xlabel('Seuil de decision')
axes[0].set_ylabel('Profit net (euros)')
axes[0].set_title('Profit net par seuil')
axes[0].legend(fontsize=9)
sns.despine(ax=axes[0])

# Clients contactes
axes[1].plot(results_df['Threshold'], results_df['Contacted'],
             color='#e74c3c', linewidth=2, label='Contactes')
axes[1].plot(results_df['Threshold'], results_df['Converted'],
             color='#2ecc71', linewidth=2, label='Convertis')
axes[1].axvline(best_threshold, color='red', linestyle='--', alpha=0.5)
axes[1].set_xlabel('Seuil de decision')
axes[1].set_ylabel('Nombre de clients')
axes[1].set_title('Contactes vs Convertis par seuil')
axes[1].legend(fontsize=9)
sns.despine(ax=axes[1])

# Precision vs Recall
axes[2].plot(results_df['Threshold'], results_df['Precision'],
             color='#4f6ef7', linewidth=2, label='Precision')
axes[2].plot(results_df['Threshold'], results_df['Recall'],
             color='#f39c12', linewidth=2, label='Recall')
axes[2].axvline(best_threshold, color='red', linestyle='--', alpha=0.5)
axes[2].set_xlabel('Seuil de decision')
axes[2].set_ylabel('Score')
axes[2].set_title('Precision vs Recall par seuil')
axes[2].legend(fontsize=9)
sns.despine(ax=axes[2])

plt.suptitle('Optimisation du seuil de decision marketing',
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('reports/figures/G_threshold_optimization.png',
            dpi=150, bbox_inches='tight')
plt.close()
print("Figure seuil sauvegardee")

# ── 3. COMPARAISON STRATEGIES ─────────────────────────────
print("\n" + "=" * 60)
print("2. COMPARAISON DES STRATEGIES DE CAMPAGNE")
print("=" * 60)

total_respondents = df_scores['y_true'].sum()
total_clients     = len(df_scores)

def compute_strategy(name, mask, y_true, cost, revenue):
    contacted  = mask.sum()
    converted  = (mask & (y_true == 1)).sum()
    profit     = (converted * revenue) - (contacted * cost)
    roi        = (profit / (contacted * cost) * 100) if contacted > 0 else 0
    precision  = converted / contacted if contacted > 0 else 0
    recall     = converted / y_true.sum() if y_true.sum() > 0 else 0
    return {
        'Strategie':  name,
        'Contactes':  contacted,
        'Convertis':  converted,
        'Profit':     round(profit, 0),
        'ROI_pct':    round(roi, 1),
        'Precision':  round(precision, 2),
        'Recall':     round(recall, 2)
    }

y_true = df_scores['y_true']
y_prob = df_scores['y_proba']

strategies = []

# Strategie 1 : tout le monde
strategies.append(compute_strategy(
    'Tous les clients',
    pd.Series([True] * len(df_scores)),
    y_true, COST_CONTACT, REVENUE_CONV))

# Strategie 2 : seuil defaut 0.5
strategies.append(compute_strategy(
    'Seuil defaut (0.50)',
    y_prob >= 0.50,
    y_true, COST_CONTACT, REVENUE_CONV))

# Strategie 3 : seuil optimal
strategies.append(compute_strategy(
    f'Seuil optimal ({best_threshold:.2f})',
    y_prob >= best_threshold,
    y_true, COST_CONTACT, REVENUE_CONV))

# Strategie 4 : top 20% scores
top20_threshold = np.percentile(y_prob, 80)
strategies.append(compute_strategy(
    'Top 20% scores',
    y_prob >= top20_threshold,
    y_true, COST_CONTACT, REVENUE_CONV))

# Strategie 5 : segment Premium Engages uniquement
if 'Segment' in df_scores.columns:
    strategies.append(compute_strategy(
        'Premium Engages uniquement',
        df_scores['Segment'] == 'Premium Engages',
        y_true, COST_CONTACT, REVENUE_CONV))

strat_df = pd.DataFrame(strategies)
print(strat_df.to_string(index=False))

# ── 4. VISUALISATION STRATEGIES ──────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
colors_s = ['#b0bec5', '#f39c12', '#4f6ef7', '#2ecc71', '#e74c3c']

# Profit par stratégie
bars = axes[0].bar(strat_df['Strategie'], strat_df['Profit'],
                   color=colors_s[:len(strat_df)], edgecolor='white')
for bar, val in zip(bars, strat_df['Profit']):
    axes[0].text(bar.get_x() + bar.get_width()/2,
                 bar.get_height() + 10,
                 f'{val:.0f}', ha='center', fontsize=9, fontweight='bold')
axes[0].axhline(0, color='black', linewidth=0.8)
axes[0].set_title('Profit net par strategie (euros)')
axes[0].set_ylabel('Profit (euros)')
axes[0].tick_params(axis='x', rotation=20)
sns.despine(ax=axes[0])

# ROI par stratégie
bars2 = axes[1].bar(strat_df['Strategie'], strat_df['ROI_pct'],
                    color=colors_s[:len(strat_df)], edgecolor='white')
for bar, val in zip(bars2, strat_df['ROI_pct']):
    axes[1].text(bar.get_x() + bar.get_width()/2,
                 bar.get_height() + 1,
                 f'{val:.0f}%', ha='center', fontsize=9, fontweight='bold')
axes[1].axhline(0, color='black', linewidth=0.8)
axes[1].set_title('ROI par strategie (%)')
axes[1].set_ylabel('ROI (%)')
axes[1].tick_params(axis='x', rotation=20)
sns.despine(ax=axes[1])

plt.suptitle('Comparaison des strategies de ciblage',
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('reports/figures/G_strategies_comparison.png',
            dpi=150, bbox_inches='tight')
plt.close()
print("Figure strategies sauvegardee")

# ── 5. SCORING PAR SEGMENT ────────────────────────────────
print("\n" + "=" * 60)
print("3. SCORING ET VALEUR PAR SEGMENT")
print("=" * 60)

segment_analysis = df_scores.groupby('Segment').agg(
    Clients=('y_true', 'count'),
    Repondants=('y_true', 'sum'),
    Score_moyen=('y_proba', 'mean'),
    Score_max=('y_proba', 'max')
).round(3)

segment_analysis['Taux_reponse'] = (
    segment_analysis['Repondants'] /
    segment_analysis['Clients'] * 100).round(1)

segment_analysis['Profit_potentiel'] = (
    segment_analysis['Repondants'] * REVENUE_CONV -
    segment_analysis['Clients'] * COST_CONTACT).round(0)

segment_analysis = segment_analysis.sort_values(
    'Profit_potentiel', ascending=False)

print(segment_analysis.to_string())

# ── 6. RECOMMANDATION FINALE ──────────────────────────────
print("\n" + "=" * 60)
print("RECOMMANDATION FINALE — DECISION MARKETING")
print("=" * 60)

best_strat = strat_df.loc[strat_df['Profit'].idxmax()]

print(f"\nStrategie recommandee : {best_strat['Strategie']}")
print(f"Clients a contacter   : {best_strat['Contactes']}")
print(f"Conversions attendues : {best_strat['Convertis']}")
print(f"Profit net attendu    : {best_strat['Profit']:.0f} euros")
print(f"ROI                   : {best_strat['ROI_pct']:.1f}%")
print(f"Precision             : {best_strat['Precision']:.2f}")
print(f"Recall                : {best_strat['Recall']:.2f}")

print("\nRegles de ciblage recommandees :")
print(f"   - Contacter les clients avec score >= {best_threshold:.2f}")
print(f"   - Prioriser le segment Premium Engages")
print(f"   - Exclure les clients avec Recency > 70 jours")
print(f"   - Budget campagne estime : {best_strat['Contactes'] * COST_CONTACT} euros")

# Extrapolation sur la base complete
ratio_test = len(df_scores) / len(df_full)
print(f"\nExtrapolation base complete ({len(df_full)} clients) :")
print(f"   Clients a cibler  : {int(best_strat['Contactes'] / ratio_test)}")
print(f"   Profit potentiel  : {int(best_strat['Profit'] / ratio_test)} euros")

# Export JSON pour le dashboard React
import json
dashboard_data = {
    'kpis': {
        'total_clients':       int(len(df_full)),
        'response_rate_global': float(round(df_full['Response'].mean() * 100, 1)),
        'best_model':          'Logistic Regression',
        'auc_roc':             0.9109,
        'optimal_threshold':   float(round(best_threshold, 2)),
        'expected_roi':        float(round(best_strat['ROI_pct'], 1)),
        'clients_to_target':   int(best_strat['Contactes']),
        'expected_profit':     int(best_strat['Profit']),
        'expected_conversions': int(best_strat['Convertis'])
    },
    'strategies': strat_df.to_dict(orient='records'),
    'segments':   segment_analysis.reset_index().to_dict(orient='records')
}

with open('frontend/src/data/kpis.json', 'w') as f:
    json.dump(dashboard_data['kpis'], f, indent=2)

with open('frontend/src/data/segments.json', 'w') as f:
    json.dump(dashboard_data['segments'], f, indent=2)

print("\nDonnees exportees pour le dashboard React")
print("   -> frontend/src/data/kpis.json")
print("   -> frontend/src/data/segments.json")

print("\n" + "=" * 60)
print("PARTIE G TERMINEE")
print("=" * 60)