import kpis from '../data/kpis.json'

const models = [
  { name: 'Logistic Regression', auc: 0.9109, recall: 0.82,
    f1: 0.60, status: 'RETENU',  color: '#10b981' },
  { name: 'Gradient Boosting',   auc: 0.9019, recall: 0.42,
    f1: 0.54, status: 'REF',     color: '#4f6ef7' },
  { name: 'Random Forest',       auc: 0.8586, recall: 0.25,
    f1: 0.38, status: 'ECARTE',  color: '#6b7280' },
  { name: 'KNN',                 auc: 0.7517, recall: 0.31,
    f1: 0.42, status: 'ECARTE',  color: '#6b7280' },
]

const shap = [
  { var: 'Recency',           val: 0.636, desc: 'Client recent = plus repondant' },
  { var: 'Seniority_Days',    val: 0.580, desc: 'Fidelite client = engagement' },
  { var: 'CmpAccepted_Total', val: 0.471, desc: 'Historique campagnes — signal fort' },
  { var: 'Is_Couple',         val: 0.352, desc: 'Situation familiale influence' },
  { var: 'MntMeatProducts',   val: 0.307, desc: 'Profil depenses premium' },
  { var: 'MntGoldProds',      val: 0.207, desc: 'Achat produits premium' },
  { var: 'Income',            val: 0.180, desc: 'Revenu — driver secondaire' },
  { var: 'NumStorePurchases', val: 0.164, desc: 'Canal magasin actif' },
]

export default function Scoring() {
  const maxShap = Math.max(...shap.map(s => s.val))

  return (
    <div style={{ padding: 'clamp(16px, 4vw, 32px)' }}>

      {/* Header */}
      <div style={{ marginBottom: '28px' }}>
        <div style={{ fontSize: '11px', color: '#4f6ef7', fontWeight: 600,
                      letterSpacing: '2px', textTransform: 'uppercase',
                      marginBottom: '8px' }}>Machine Learning</div>
        <h1 style={{ fontSize: 'clamp(20px, 4vw, 28px)', fontWeight: 700,
                     color: '#fff', margin: 0 }}>Scoring ML</h1>
        <p style={{ fontSize: '14px', color: 'rgba(255,255,255,0.4)',
                    marginTop: '6px' }}>
          Comparaison des modeles et explicabilite SHAP
        </p>
      </div>

      {/* Comparaison modeles */}
      <div style={{
        background: 'linear-gradient(135deg, #0d1526 0%, #111827 100%)',
        border: '1px solid rgba(79,110,247,0.15)',
        borderRadius: '12px', padding: '24px', marginBottom: '20px',
        overflowX: 'auto'
      }}>
        <div style={{ fontSize: '11px', color: '#4f6ef7', fontWeight: 600,
                      letterSpacing: '2px', textTransform: 'uppercase',
                      marginBottom: '20px' }}>Comparaison des modeles</div>

        <div style={{ display: 'flex', flexDirection: 'column',
                      gap: '12px', minWidth: '400px' }}>
          {models.map((m, i) => (
            <div key={i} style={{
              display: 'grid',
              gridTemplateColumns: '180px 1fr 80px 80px 100px',
              alignItems: 'center', gap: '16px',
              padding: '14px 16px', borderRadius: '8px',
              background: m.status === 'RETENU'
                ? 'rgba(16,185,129,0.08)' : 'rgba(255,255,255,0.03)',
              border: m.status === 'RETENU'
                ? '1px solid rgba(16,185,129,0.25)' : '1px solid transparent'
            }}>
              <div style={{ fontSize: '13px', fontWeight: 600,
                            color: m.status === 'ECARTE'
                              ? 'rgba(255,255,255,0.3)' : '#fff' }}>
                {m.name}
              </div>
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between',
                              fontSize: '10px', marginBottom: '4px' }}>
                  <span style={{ color: 'rgba(255,255,255,0.35)' }}>AUC-ROC</span>
                  <span style={{ color: m.color, fontWeight: 700 }}>{m.auc}</span>
                </div>
                <div style={{ background: 'rgba(255,255,255,0.06)',
                              borderRadius: '4px', height: '5px' }}>
                  <div style={{ width: `${m.auc * 100}%`, height: '100%',
                                background: m.color, borderRadius: '4px' }}/>
                </div>
              </div>
              <div style={{ textAlign: 'center' }}>
                <div style={{ fontSize: '10px', color: 'rgba(255,255,255,0.35)',
                              marginBottom: '2px' }}>Recall</div>
                <div style={{ fontSize: '14px', fontWeight: 700,
                              color: m.color }}>{m.recall}</div>
              </div>
              <div style={{ textAlign: 'center' }}>
                <div style={{ fontSize: '10px', color: 'rgba(255,255,255,0.35)',
                              marginBottom: '2px' }}>F1</div>
                <div style={{ fontSize: '14px', fontWeight: 700,
                              color: 'rgba(255,255,255,0.6)' }}>{m.f1}</div>
              </div>
              <div style={{ textAlign: 'center' }}>
                <span style={{
                  background: m.color + '22', color: m.color,
                  border: `1px solid ${m.color}44`,
                  borderRadius: '20px', padding: '4px 10px',
                  fontSize: '10px', fontWeight: 700
                }}>{m.status}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* SHAP */}
      <div style={{
        background: 'linear-gradient(135deg, #0d1526 0%, #111827 100%)',
        border: '1px solid rgba(79,110,247,0.15)',
        borderRadius: '12px', padding: '24px'
      }}>
        <div style={{ fontSize: '11px', color: '#4f6ef7', fontWeight: 600,
                      letterSpacing: '2px', textTransform: 'uppercase',
                      marginBottom: '20px' }}>
          Importance des variables — SHAP
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
          {shap.map((s, i) => (
            <div key={i}>
              <div style={{ display: 'flex', justifyContent: 'space-between',
                            alignItems: 'center', marginBottom: '6px' }}>
                <div>
                  <span style={{ fontSize: '13px', fontWeight: 600,
                                 color: '#fff' }}>{s.var}</span>
                  <span style={{ fontSize: '11px',
                                 color: 'rgba(255,255,255,0.35)',
                                 marginLeft: '10px' }}>{s.desc}</span>
                </div>
                <span style={{ fontSize: '13px', fontWeight: 700,
                               color: '#4f6ef7', minWidth: '40px',
                               textAlign: 'right' }}>{s.val}</span>
              </div>
              <div style={{ background: 'rgba(255,255,255,0.06)',
                            borderRadius: '4px', height: '6px' }}>
                <div style={{
                  width: `${(s.val / maxShap) * 100}%`,
                  height: '100%', borderRadius: '4px',
                  background: `linear-gradient(90deg, #4f6ef7, #a78bfa)`,
                  transition: 'width 0.6s ease'
                }}/>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}