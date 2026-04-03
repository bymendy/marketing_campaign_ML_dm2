import kpis from '../data/kpis.json'

const useIsMobile = () => window.innerWidth < 768

const KPI = ({ value, label, sub, color = '#4f6ef7' }) => (
  <div style={{
    background: 'linear-gradient(135deg, #0d1526 0%, #111827 100%)',
    border: '1px solid rgba(79,110,247,0.15)',
    borderRadius: '12px', padding: '20px',
    display: 'flex', flexDirection: 'column', gap: '6px',
    position: 'relative', overflow: 'hidden', minWidth: 0
  }}>
    <div style={{
      position: 'absolute', top: 0, left: 0,
      width: '3px', height: '100%',
      background: color, borderRadius: '12px 0 0 12px'
    }}/>
    <div style={{
      fontSize: 'clamp(20px, 5vw, 28px)', fontWeight: 700,
      color, letterSpacing: '-0.5px', lineHeight: 1,
      wordBreak: 'break-word'
    }}>{value}</div>
    <div style={{
      fontSize: 'clamp(9px, 2vw, 11px)', fontWeight: 600,
      color: 'rgba(255,255,255,0.7)',
      textTransform: 'uppercase', letterSpacing: '1px'
    }}>{label}</div>
    {sub && <div style={{
      fontSize: '11px', color: 'rgba(255,255,255,0.3)'
    }}>{sub}</div>}
  </div>
)

const Badge = ({ text, color }) => (
  <span style={{
    background: color + '22', color,
    border: `1px solid ${color}44`,
    borderRadius: '20px', padding: '4px 10px',
    fontSize: '11px', fontWeight: 600, letterSpacing: '0.5px',
    whiteSpace: 'nowrap'
  }}>{text}</span>
)

export default function Overview() {
  return (
    <div style={{ padding: 'clamp(16px, 5vw, 32px)' }}>

      {/* Header */}
      <div style={{ marginBottom: '24px' }}>
        <div style={{
          fontSize: '11px', color: '#4f6ef7', fontWeight: 600,
          letterSpacing: '2px', textTransform: 'uppercase', marginBottom: '8px'
        }}>Tableau de bord</div>
        <h1 style={{
          fontSize: 'clamp(22px, 5vw, 28px)', fontWeight: 700,
          color: '#fff', margin: 0, letterSpacing: '-0.5px'
        }}>Vue generale</h1>
        <p style={{
          fontSize: '13px', color: 'rgba(255,255,255,0.4)', marginTop: '6px'
        }}>Pipeline ML marketing — resultats et performance globale</p>
      </div>

      {/* KPI Grid ligne 1 — 2 colonnes sur mobile, 4 sur desktop */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(2, 1fr)',
        gap: '12px', marginBottom: '12px'
      }}>
        <KPI value={kpis.total_clients.toLocaleString()}
             label="Clients analyses"
             sub="Dataset complet"
             color="#4f6ef7" />
        <KPI value={`${kpis.response_rate_global}%`}
             label="Taux reponse"
             sub="Variable cible"
             color="#f59e0b" />
        <KPI value={kpis.auc_roc}
             label="AUC-ROC"
             sub="Meilleur modele"
             color="#10b981" />
        <KPI value={`${kpis.expected_roi}%`}
             label="ROI attendu"
             sub="Strategie optimale"
             color="#a78bfa" />
      </div>

      {/* KPI Grid ligne 2 */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(2, 1fr)',
        gap: '12px', marginBottom: '20px'
      }}>
        <KPI value={kpis.clients_to_target}
             label="Clients a cibler"
             sub={`Seuil ${kpis.optimal_threshold}`}
             color="#4f6ef7" />
        <KPI value="4 720 eur"
             label="Profit net test"
             sub="443 clients test"
             color="#10b981" />
        <div style={{
          gridColumn: '1 / -1',
          background: 'linear-gradient(135deg, #0d1526 0%, #111827 100%)',
          border: '1px solid rgba(16,185,129,0.25)',
          borderRadius: '12px', padding: '20px',
          display: 'flex', alignItems: 'center',
          justifyContent: 'space-between', gap: '16px',
          position: 'relative', overflow: 'hidden'
        }}>
          <div style={{
            position: 'absolute', top: 0, left: 0,
            width: '3px', height: '100%',
            background: '#10b981'
          }}/>
          <div>
            <div style={{
              fontSize: 'clamp(18px, 5vw, 26px)', fontWeight: 700,
              color: '#10b981', lineHeight: 1
            }}>23 568 eur</div>
            <div style={{
              fontSize: '10px', fontWeight: 600,
              color: 'rgba(255,255,255,0.5)',
              textTransform: 'uppercase', letterSpacing: '1px',
              marginTop: '4px'
            }}>Profit extrapole</div>
            <div style={{ fontSize: '11px',
                          color: 'rgba(255,255,255,0.3)', marginTop: '2px' }}>
              Base complete 2212 clients
            </div>
          </div>
          <div style={{
            background: 'rgba(16,185,129,0.1)',
            border: '1px solid rgba(16,185,129,0.25)',
            borderRadius: '8px', padding: '10px 16px', textAlign: 'center',
            flexShrink: 0
          }}>
            <div style={{ fontSize: '20px', fontWeight: 700,
                          color: '#10b981' }}>299%</div>
            <div style={{ fontSize: '10px',
                          color: 'rgba(255,255,255,0.4)',
                          textTransform: 'uppercase', letterSpacing: '1px' }}>ROI</div>
          </div>
        </div>
      </div>

      {/* Modele retenu */}
      <div style={{
        background: 'linear-gradient(135deg, #0d1526 0%, #111827 100%)',
        border: '1px solid rgba(79,110,247,0.15)',
        borderRadius: '12px', padding: '20px', marginBottom: '16px'
      }}>
        <div style={{
          fontSize: '11px', color: '#4f6ef7', fontWeight: 600,
          letterSpacing: '2px', textTransform: 'uppercase', marginBottom: '12px'
        }}>Modele retenu</div>
        <div style={{
          fontSize: 'clamp(16px, 4vw, 20px)', fontWeight: 700,
          color: '#fff', marginBottom: '4px'
        }}>{kpis.best_model}</div>
        <div style={{
          fontSize: '13px', color: 'rgba(255,255,255,0.4)', marginBottom: '14px'
        }}>Meilleur compromis AUC + Recall repondants</div>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
          <Badge text={`AUC ${kpis.auc_roc}`}    color="#10b981" />
          <Badge text="Recall 0.82"               color="#4f6ef7" />
          <Badge text={`Seuil ${kpis.optimal_threshold}`} color="#f59e0b" />
          <Badge text="class_weight balanced"     color="#a78bfa" />
        </div>
      </div>

      {/* Pipeline ML */}
      <div style={{
        background: 'linear-gradient(135deg, #0d1526 0%, #111827 100%)',
        border: '1px solid rgba(79,110,247,0.15)',
        borderRadius: '12px', padding: '20px'
      }}>
        <div style={{
          fontSize: '11px', color: '#4f6ef7', fontWeight: 600,
          letterSpacing: '2px', textTransform: 'uppercase', marginBottom: '16px'
        }}>Pipeline ML</div>

        {/* Desktop : horizontal */}
        <div style={{
          display: 'flex', alignItems: 'center', gap: '0',
          overflowX: 'auto', paddingBottom: '4px'
        }}>
          {[
            { label: 'Audit',        sub: 'Partie A', color: '#4f6ef7' },
            { label: 'Preparation',  sub: 'Partie B', color: '#4f6ef7' },
            { label: 'EDA',          sub: 'Partie C', color: '#4f6ef7' },
            { label: 'Segmentation', sub: 'Partie D', color: '#10b981' },
            { label: 'Modelisation', sub: 'Partie F', color: '#10b981' },
            { label: 'Decision',     sub: 'Partie G', color: '#a78bfa' },
          ].map((step, i, arr) => (
            <div key={i} style={{ display: 'flex', alignItems: 'center',
                                  flex: 1, minWidth: '80px' }}>
              <div style={{
                flex: 1, textAlign: 'center',
                background: step.color + '15',
                border: `1px solid ${step.color}44`,
                borderRadius: '8px', padding: '10px 6px'
              }}>
                <div style={{ fontSize: 'clamp(10px, 2vw, 12px)',
                              fontWeight: 700, color: step.color }}>
                  {step.label}
                </div>
                <div style={{ fontSize: '10px',
                              color: 'rgba(255,255,255,0.3)', marginTop: '2px' }}>
                  {step.sub}
                </div>
              </div>
              {i < arr.length - 1 && (
                <div style={{ color: 'rgba(255,255,255,0.2)',
                              fontSize: '14px', padding: '0 3px',
                              flexShrink: 0 }}>›</div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}