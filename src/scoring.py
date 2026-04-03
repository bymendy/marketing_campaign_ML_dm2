# ============================================================
# Partie H - Scalabilité, industrialisation et MLOps
# ============================================================

import pandas as pd
import numpy as np
import joblib
import json
import yaml
import warnings
from datetime import datetime

warnings.filterwarnings('ignore')

print("=" * 60)
print("PARTIE H — MLOPS ET INDUSTRIALISATION")
print("=" * 60)

# ── 1. PIPELINE DE SCORING INDUSTRIEL ────────────────────
print("\n1. PIPELINE DE SCORING")
print("-" * 40)

def score_new_clients(df_new, scaler_path, model_path, threshold_path):
    """
    Pipeline de scoring industrialisable.
    Prend un dataframe brut, retourne les scores et decisions.
    """
    # Chargement modele et scaler
    scaler    = joblib.load(scaler_path)
    model     = joblib.load(model_path)

    with open(threshold_path, 'r') as f:
        config    = yaml.safe_load(f)
    threshold = config.get('optimized_threshold', 0.07)

    # Features attendues
    exclude  = ['Response', 'Cluster', 'Segment', 'Education']
    features = [c for c in df_new.columns if c not in exclude]

    # Scoring
    X_scaled  = scaler.transform(df_new[features])
    scores    = model.predict_proba(X_scaled)[:, 1]
    decisions = (scores >= threshold).astype(int)

    # Output
    df_output = df_new.copy()
    df_output['score_proba']  = scores.round(4)
    df_output['decision']     = decisions
    df_output['scored_at']    = datetime.now().strftime('%Y-%m-%d %H:%M')
    df_output['threshold']    = threshold

    return df_output

# Test du pipeline sur le jeu de test existant
df_test = pd.read_csv('data/processed/df_scores.csv')
exclude_cols = ['y_true', 'y_proba', 'y_pred', 'Cluster', 'Segment',
                'Response', 'Education']
df_input = df_test.drop(
    columns=[c for c in exclude_cols if c in df_test.columns])

df_scored = score_new_clients(
    df_input,
    scaler_path    = 'models/scaler.pkl',
    model_path     = 'models/best_model.pkl',
    threshold_path = 'configs/thresholds.yaml'
)

print(f"Pipeline de scoring operationnel")
print(f"Clients scores          : {len(df_scored)}")
print(f"Clients a contacter     : {df_scored['decision'].sum()}")
print(f"Score moyen             : {df_scored['score_proba'].mean():.3f}")
print(f"Score max               : {df_scored['score_proba'].max():.3f}")

# ── 2. LIMITES ACTUELLES ─────────────────────────────────
print("\n" + "=" * 60)
print("2. LIMITES DES METHODES ACTUELLES")
print("=" * 60)

limites = {
    "Volume de donnees": [
        "2212 observations : faible pour du deep learning",
        "Pas de donnees temps reel : scoring batch uniquement",
        "Pas de variable geographique : segmentation incomplete",
    ],
    "Modele": [
        "Modele statique : pas de reapprentissage automatique",
        "Pas de gestion du concept drift",
        "Features engineering manuel : non automatise",
        "Pas de versioning modele (MLflow, DVC)",
    ],
    "Infrastructure": [
        "Execution locale : non scalable au-dela de 100K clients",
        "Pas d'API de scoring : integration manuelle",
        "Pas de monitoring en production",
    ]
}

for categorie, points in limites.items():
    print(f"\n{categorie} :")
    for p in points:
        print(f"   - {p}")

# ── 3. VISION INDUSTRIALISATION ───────────────────────────
print("\n" + "=" * 60)
print("3. PISTES D INDUSTRIALISATION")
print("=" * 60)

roadmap = {
    "Court terme (1-3 mois)": [
        "Exposer le modele via une API REST (FastAPI)",
        "Dockeriser le pipeline de scoring",
        "Mettre en place MLflow pour le versioning des modeles",
        "Automatiser le feature engineering avec sklearn Pipeline",
    ],
    "Moyen terme (3-6 mois)": [
        "Connecter a la base de donnees clients en temps reel",
        "Scheduler le reapprentissage mensuel (Airflow/cron)",
        "Dashboard monitoring des performances modele",
        "A/B testing des strategies de ciblage",
    ],
    "Long terme (6-12 mois)": [
        "Migration vers un feature store centralise",
        "Modeles en temps reel (streaming scoring)",
        "Personnalisation individuelle des offres",
        "Integration CRM automatique (Salesforce, HubSpot)",
    ]
}

for phase, actions in roadmap.items():
    print(f"\n{phase} :")
    for a in actions:
        print(f"   - {a}")

# ── 4. DETECTION DERIVE DES DONNEES ──────────────────────
print("\n" + "=" * 60)
print("4. SUIVI DE DERIVE — DATA DRIFT MONITORING")
print("=" * 60)

def compute_drift_report(df_reference, df_new, features, threshold=0.1):
    """
    Detection simple de derive des donnees.
    Compare les moyennes et ecarts-types entre reference et nouvelles donnees.
    Alerte si deviation > threshold.
    """
    report = []
    for feat in features:
        if feat not in df_reference.columns or feat not in df_new.columns:
            continue
        mean_ref = df_reference[feat].mean()
        mean_new = df_new[feat].mean()
        std_ref  = df_reference[feat].std()

        deviation = abs(mean_new - mean_ref) / (std_ref + 1e-8)
        drift     = deviation > threshold

        report.append({
            'Feature':    feat,
            'Mean_ref':   round(mean_ref, 3),
            'Mean_new':   round(mean_new, 3),
            'Deviation':  round(deviation, 3),
            'Drift':      'ALERTE' if drift else 'OK'
        })

    return pd.DataFrame(report).sort_values('Deviation', ascending=False)

# Simulation : on simule des nouvelles donnees avec derive legere
df_ref = pd.read_csv('data/processed/df_clustered.csv')
df_sim = df_ref.copy()

# Simulation derive : revenu augmente de 15%, recency augmente de 20%
df_sim['Income']  = df_sim['Income']  * 1.15
df_sim['Recency'] = df_sim['Recency'] * 1.20

drift_features = ['Income', 'Recency', 'TotalSpend', 'Age',
                  'CmpAccepted_Total', 'TotalChildren']

drift_report = compute_drift_report(df_ref, df_sim, drift_features)
print("\nRapport de derive (simulation) :")
print(drift_report.to_string(index=False))

# ── 5. POLITIQUE DE REAPPRENTISSAGE ──────────────────────
print("\n" + "=" * 60)
print("5. POLITIQUE DE REAPPRENTISSAGE")
print("=" * 60)

politique = [
    "Frequence : reapprentissage mensuel ou si AUC baisse de > 3 points",
    "Declencheur : drift detecte sur > 2 features critiques",
    "Validation : AUC test >= 0.88 avant mise en production",
    "Rollback : conserver les 3 derniers modeles en production",
    "Monitoring : alertes automatiques si taux conversion < seuil attendu",
]

for p in politique:
    print(f"   - {p}")

# ── 6. ARCHITECTURE CIBLE ────────────────────────────────
print("\n" + "=" * 60)
print("6. ARCHITECTURE CIBLE DE PRODUCTION")
print("=" * 60)

architecture = """
[Source donnees CRM]
        |
        v
[Feature Store] --> [Pipeline preprocessing automatise]
        |
        v
[Modele ML en production] --> [API REST scoring]
        |                              |
        v                              v
[Monitoring drift]            [Dashboard marketing]
        |                              |
        v                              v
[Reapprentissage auto]        [CRM / Actions campagne]
"""
print(architecture)

# ── 7. SAUVEGARDE RAPPORT MLOPS ──────────────────────────
mlops_report = {
    'date':          datetime.now().strftime('%Y-%m-%d'),
    'modele':        'Gradient Boosting optimise',
    'auc_production': 0.9019,
    'seuil':         0.07,
    'pipeline':      'operationnel',
    'drift_monitor': 'simule',
    'next_retrain':  'mensuel',
}

with open('reports/mlops_report.json', 'w') as f:
    json.dump(mlops_report, f, indent=2)

print("Rapport MLOps sauvegarde -> reports/mlops_report.json")

print("\n" + "=" * 60)
print("PARTIE H TERMINEE")
print("=" * 60)