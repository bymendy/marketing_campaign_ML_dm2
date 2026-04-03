# ============================================================
# Partie F - Modelisation predictive de la reponse campagne
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import joblib

from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (classification_report, roc_auc_score,
                             roc_curve, average_precision_score)
from sklearn.model_selection import GridSearchCV
import shap

warnings.filterwarnings('ignore')

# ── Chargement ───────────────────────────────────────────
df = pd.read_csv('data/processed/df_clustered.csv')
print(f"Dataset charge : {df.shape[0]} lignes x {df.shape[1]} colonnes")
print(f"Taux de reponse global : {df['Response'].mean()*100:.1f}%")

# ── Preparation ──────────────────────────────────────────
exclude = ['Response', 'Cluster', 'Segment', 'Education']
features = [c for c in df.columns if c not in exclude]

X = df[features]
y = df['Response']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

joblib.dump(scaler, 'models/scaler.pkl')
print(f"Train : {X_train.shape[0]} | Test : {X_test.shape[0]}")

# ── Cross-validation 4 modeles ───────────────────────────
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

models = {
    'Logistic Regression': LogisticRegression(
        class_weight='balanced', random_state=42, max_iter=1000),
    'Random Forest': RandomForestClassifier(
        class_weight='balanced', random_state=42, n_estimators=100),
    'Gradient Boosting': GradientBoostingClassifier(
        random_state=42, n_estimators=100),
    'KNN': KNeighborsClassifier(n_neighbors=5)
}

print("\n" + "=" * 60)
print("COMPARAISON MODELES — CROSS VALIDATION")
print("=" * 60)

results = {}
for name, model in models.items():
    auc_scores = cross_val_score(
        model, X_train_scaled, y_train,
        cv=cv, scoring='roc_auc', n_jobs=-1)
    f1_scores = cross_val_score(
        model, X_train_scaled, y_train,
        cv=cv, scoring='f1', n_jobs=-1)
    results[name] = {
        'AUC_mean': auc_scores.mean(),
        'AUC_std':  auc_scores.std(),
        'F1_mean':  f1_scores.mean(),
        'model':    model
    }
    print(f"\n{name}")
    print(f"   AUC-ROC : {auc_scores.mean():.4f} (+/- {auc_scores.std():.4f})")
    print(f"   F1      : {f1_scores.mean():.4f}")

# ── Evaluation test set ──────────────────────────────────
print("\n" + "=" * 60)
print("EVALUATION SUR LE JEU DE TEST")
print("=" * 60)

test_results = {}
for name, res in results.items():
    try:
        model   = res['model']
        model.fit(X_train_scaled, y_train)
        y_pred  = model.predict(X_test_scaled)
        y_proba = model.predict_proba(X_test_scaled)[:, 1]
        auc     = roc_auc_score(y_test, y_proba)
        ap      = average_precision_score(y_test, y_proba)
        test_results[name] = {
            'AUC': auc, 'AP': ap,
            'y_proba': y_proba, 'y_pred': y_pred, 'model': model
        }
        print(f"\n{name}")
        print(f"   AUC-ROC           : {auc:.4f}")
        print(f"   Average Precision : {ap:.4f}")
        print(classification_report(y_test, y_pred,
              target_names=['Non repondant', 'Repondant']))
    except Exception as e:
        print(f"   ERREUR sur {name} : {e}")

print("DEBUG : evaluation terminee, debut GridSearch")

# ── Courbes ROC ──────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 6))
colors = ['#4f6ef7', '#2ecc71', '#e74c3c', '#f39c12']
for (name, res), color in zip(test_results.items(), colors):
    fpr, tpr, _ = roc_curve(y_test, res['y_proba'])
    ax.plot(fpr, tpr, color=color, linewidth=2,
            label=f"{name} (AUC={res['AUC']:.3f})")
ax.plot([0, 1], [0, 1], 'k--', linewidth=1)
ax.set_xlabel('Taux faux positifs')
ax.set_ylabel('Taux vrais positifs')
ax.set_title('Courbes ROC')
ax.legend(fontsize=9)
sns.despine(ax=ax)
plt.tight_layout()
plt.savefig('reports/figures/F_roc_curves.png', dpi=150, bbox_inches='tight')
plt.close()
print("Courbes ROC sauvegardees")

# ── GridSearch Gradient Boosting ─────────────────────────
try:
    print("\n" + "=" * 60)
    print("GRIDSEARCH — GRADIENT BOOSTING")
    print("=" * 60)
    print("En cours... (2-3 minutes)")

    param_grid = {
        'n_estimators':  [100, 200],
        'max_depth':     [3, 4],
        'learning_rate': [0.05, 0.1],
        'subsample':     [0.8, 1.0]
    }

    gb_base     = GradientBoostingClassifier(random_state=42)
    grid_search = GridSearchCV(
        gb_base, param_grid, cv=cv,
        scoring='roc_auc', n_jobs=-1, verbose=0)
    grid_search.fit(X_train_scaled, y_train)

    print(f"Meilleurs parametres : {grid_search.best_params_}")
    print(f"Meilleur AUC CV      : {grid_search.best_score_:.4f}")

    best_model   = grid_search.best_estimator_
    y_pred_best  = best_model.predict(X_test_scaled)
    y_proba_best = best_model.predict_proba(X_test_scaled)[:, 1]

    print(f"AUC-ROC Test (optimise) : {roc_auc_score(y_test, y_proba_best):.4f}")
    print(classification_report(y_test, y_pred_best,
          target_names=['Non repondant', 'Repondant']))

    joblib.dump(best_model, 'models/gradient_boosting_optimized.pkl')
    joblib.dump(best_model, 'models/best_model.pkl')
    print("Modele GB optimise sauvegarde")

except Exception as e:
    import traceback
    print(f"ERREUR GridSearch : {e}")
    traceback.print_exc()
    print("\nFallback : Logistic Regression retenue comme best_model")
    best_model   = test_results['Logistic Regression']['model']
    y_proba_best = test_results['Logistic Regression']['y_proba']
    y_pred_best  = test_results['Logistic Regression']['y_pred']
    joblib.dump(best_model, 'models/best_model.pkl')
    print("Modele sauvegarde -> models/best_model.pkl")

# ── SHAP ─────────────────────────────────────────────────
print("\nCalcul SHAP en cours...")
try:
    explainer    = shap.TreeExplainer(best_model)
    shap_values  = explainer.shap_values(X_test_scaled)

    shap_importance = pd.DataFrame({
        'Variable':        features,
        'SHAP_importance': np.abs(shap_values).mean(axis=0)
    }).sort_values('SHAP_importance', ascending=False)

    print("\nTop 10 variables (SHAP) :")
    print(shap_importance.head(10).to_string(index=False))

    fig, ax = plt.subplots(figsize=(8, 6))
    top10 = shap_importance.head(10)
    ax.barh(top10['Variable'][::-1],
            top10['SHAP_importance'][::-1], color='#4f6ef7')
    ax.set_title('Top 10 variables - Importance SHAP')
    ax.set_xlabel('Importance SHAP moyenne')
    sns.despine(ax=ax)
    plt.tight_layout()
    plt.savefig('reports/figures/F_shap_importance.png',
                dpi=150, bbox_inches='tight')
    plt.close()
    print("Figure SHAP sauvegardee")
except Exception as e:
    print(f"ERREUR SHAP : {e}")

# ── Sauvegarde scores ────────────────────────────────────
print("\nSauvegarde des scores...")
X_test_df             = X_test.copy()
X_test_df['y_true']   = y_test.values
X_test_df['y_proba']  = y_proba_best
X_test_df['y_pred']   = y_pred_best
X_test_df['Cluster']  = df.loc[X_test.index, 'Cluster'].values
X_test_df['Segment']  = df.loc[X_test.index, 'Segment'].values
X_test_df.to_csv('data/processed/df_scores.csv', index=False)
print("Scores sauvegardes -> data/processed/df_scores.csv")

print("\n" + "=" * 60)
print("PARTIE F TERMINEE")
print("=" * 60)