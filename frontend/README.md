# Campaign Intelligence Dashboard

Dashboard React pour visualiser les résultats du pipeline ML marketing.

## Stack
- React 18 + Vite
- Tailwind CSS
- Recharts (graphiques)
- Lucide React (icônes)

## Pages
- **Overview** — KPIs globaux de la campagne
- **Segments** — Profils des clusters clients
- **Scoring** — Distribution des scores de probabilité
- **Decision** — Seuil optimal et stratégie de ciblage

## Lancement
```bash
cd frontend
npm install
npm run dev
```

## Connexion au backend Python
Les données arrivent via des fichiers JSON exportés depuis les notebooks :
- `src/data/segments.json` — résultats clustering
- `src/data/scores.json` — probabilités prédites
- `src/data/kpis.json` — métriques business
