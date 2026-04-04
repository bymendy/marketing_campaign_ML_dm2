import segments from '../data/segments.json'

const COLORS = ['#4f6ef7', '#10b981', '#f59e0b', '#e74c3c']

const bar = (val, max, color) => (
  <div style={{ background: 'rgba(255,255,255,0.06)',
                borderRadius: '4px', height: '6px', width: '100%' }}>
    <div style={{ width: `${(val/max)*100}%`, height: '100%',
                  background: color, borderRadius: '4px',
                  transition: 'width 0.6s ease' }}/>
  </div>
)

export default function Segments() {
  const maxRevenue  = Math.max(...segments.map(s => s.Revenue || s.revenue || 0))
  const maxResponse = Math.max(...segments.map(s => s.Taux_reponse || s.response_rate || 0))
  const maxSize     = Math.max(...segments.map(s => s.Clients || s.size || 0))

  return (
    <div style={{ padding: 'clamp(16px, 4vw, 32px)' }}>

      {/* Header */}
      <div style={{ marginBottom: '28px' }}>
        <div style={{ fontSize: '11px', color: '#4f6ef7', fontWeight: 600,
                      letterSpacing: '2px', textTransform: 'uppercase',
                      marginBottom: '8px' }}>Segmentation K-Means k=4</div>
        <h1 style={{ fontSize: 'clamp(20px, 4vw, 28px)', fontWeight: 700,
                     color: '#fff', margin: 0 }}>Segments clients</h1>
        <p style={{ fontSize: '14px', color: 'rgba(255,255,255,0.4)', marginTop: '6px' }}>
          4 segments identifies — profils et actions marketing differencies
        </p>
      </div>

      {/* Cards segments */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
        gap: '16px', marginBottom: '28px'
      }}>
        {segments.map((seg, i) => {
          const color    = COLORS[i % COLORS.length]
          const name     = seg.Segment || seg.label || `Segment ${i}`
          const clients  = seg.Clients || seg.size || 0
          const revenue  = seg.Revenue || seg.revenue || 0
          const response = seg.Taux_reponse || (seg.response_rate * 100) || 0
          const score    = seg.Score_moyen || 0
          const profit   = seg.Profit_potentiel || 0

          const actions = {
            'Premium Engages': 'Ciblage prioritaire — offres VIP exclusives',
            'Aises Passifs':   'Activation — campagnes personnalisees vins/viandes',
            'Actifs Moyens':   'Nurturing — promotions et cross-sell',
            'Petits Budgets':  'Low-cost — deals uniquement, ROI negatif',
          }

          const priorities = {
            'Premium Engages': { label: 'PRIORITAIRE', color: '#10b981' },
            'Aises Passifs':   { label: 'A ACTIVER',   color: '#f59e0b' },
            'Actifs Moyens':   { label: 'NURTURING',   color: '#4f6ef7' },
            'Petits Budgets':  { label: 'FAIBLE PRIO', color: '#6b7280' },
          }

          const prio = priorities[name] || { label: 'ANALYSER', color: '#6b7280' }

          return (
            <div key={i} style={{
              background: 'linear-gradient(135deg, #0d1526 0%, #111827 100%)',
              border: `1px solid ${color}33`,
              borderRadius: '12px', padding: '24px',
              position: 'relative', overflow: 'hidden'
            }}>
              <div style={{ position: 'absolute', top: 0, left: 0,
                            width: '3px', height: '100%',
                            background: color, borderRadius: '12px 0 0 12px' }}/>

              <div style={{ display: 'flex', justifyContent: 'space-between',
                            alignItems: 'flex-start', marginBottom: '16px' }}>
                <div>
                  <div style={{ fontSize: '16px', fontWeight: 700,
                                color: '#fff', marginBottom: '4px' }}>{name}</div>
                  <div style={{ fontSize: '12px', color: 'rgba(255,255,255,0.35)' }}>
                    {clients} clients
                  </div>
                </div>
                <span style={{
                  background: prio.color + '22', color: prio.color,
                  border: `1px solid ${prio.color}44`,
                  borderRadius: '20px', padding: '4px 10px',
                  fontSize: '10px', fontWeight: 700, letterSpacing: '0.5px'
                }}>{prio.label}</span>
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between',
                                fontSize: '11px', marginBottom: '6px' }}>
                    <span style={{ color: 'rgba(255,255,255,0.4)' }}>Taux reponse</span>
                    <span style={{ color, fontWeight: 700 }}>{response.toFixed(1)}%</span>
                  </div>
                  {bar(response, maxResponse, color)}
                </div>

                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between',
                                fontSize: '11px', marginBottom: '6px' }}>
                    <span style={{ color: 'rgba(255,255,255,0.4)' }}>Taille segment</span>
                    <span style={{ color: 'rgba(255,255,255,0.7)', fontWeight: 600 }}>
                      {clients}
                    </span>
                  </div>
                  {bar(clients, maxSize, color + '88')}
                </div>

                {score > 0 && (
                  <div>
                    <div style={{ display: 'flex', justifyContent: 'space-between',
                                  fontSize: '11px', marginBottom: '6px' }}>
                      <span style={{ color: 'rgba(255,255,255,0.4)' }}>Score ML moyen</span>
                      <span style={{ color: 'rgba(255,255,255,0.7)', fontWeight: 600 }}>
                        {score.toFixed(3)}
                      </span>
                    </div>
                    {bar(score, 1, '#a78bfa88')}
                  </div>
                )}

                <div style={{
                  background: 'rgba(255,255,255,0.04)',
                  borderRadius: '8px', padding: '10px 12px',
                  fontSize: '11px', color: 'rgba(255,255,255,0.5)',
                  lineHeight: 1.5, marginTop: '4px'
                }}>
                  {actions[name] || 'Action a definir'}
                </div>

                {profit !== 0 && (
                  <div style={{
                    display: 'flex', justifyContent: 'space-between',
                    alignItems: 'center', paddingTop: '8px',
                    borderTop: '1px solid rgba(255,255,255,0.06)'
                  }}>
                    <span style={{ fontSize: '11px',
                                   color: 'rgba(255,255,255,0.4)' }}>
                      Profit potentiel
                    </span>
                    <span style={{
                      fontSize: '14px', fontWeight: 700,
                      color: profit > 0 ? '#10b981' : '#e74c3c'
                    }}>
                      {profit > 0 ? '+' : ''}{profit.toLocaleString()} eur
                    </span>
                  </div>
                )}
              </div>
            </div>
          )
        })}
      </div>

      {/* Tableau recap */}
      <div style={{
        background: 'linear-gradient(135deg, #0d1526 0%, #111827 100%)',
        border: '1px solid rgba(79,110,247,0.15)',
        borderRadius: '12px', padding: '24px', overflowX: 'auto'
      }}>
        <div style={{ fontSize: '11px', color: '#4f6ef7', fontWeight: 600,
                      letterSpacing: '2px', textTransform: 'uppercase',
                      marginBottom: '16px' }}>Tableau recapitulatif</div>
        <table style={{ width: '100%', borderCollapse: 'collapse',
                        fontSize: '13px', minWidth: '500px' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.08)' }}>
              {['Segment','Clients','Taux reponse','Score ML','Profit'].map(h => (
                <th key={h} style={{ padding: '10px 12px', textAlign: 'left',
                                     fontSize: '10px', fontWeight: 600,
                                     color: 'rgba(255,255,255,0.35)',
                                     textTransform: 'uppercase',
                                     letterSpacing: '1px' }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {segments.map((seg, i) => {
              const color    = COLORS[i % COLORS.length]
              const name     = seg.Segment || seg.label
              const clients  = seg.Clients || seg.size || 0
              const response = seg.Taux_reponse || (seg.response_rate * 100) || 0
              const score    = seg.Score_moyen || 0
              const profit   = seg.Profit_potentiel || 0
              return (
                <tr key={i} style={{
                  borderBottom: '1px solid rgba(255,255,255,0.04)',
                  transition: 'background 0.15s'
                }}>
                  <td style={{ padding: '12px', color: '#fff', fontWeight: 600 }}>
                    <span style={{ display: 'inline-block', width: '8px',
                                   height: '8px', borderRadius: '50%',
                                   background: color, marginRight: '8px' }}/>
                    {name}
                  </td>
                  <td style={{ padding: '12px',
                               color: 'rgba(255,255,255,0.6)' }}>{clients}</td>
                  <td style={{ padding: '12px', color, fontWeight: 700 }}>
                    {response.toFixed(1)}%
                  </td>
                  <td style={{ padding: '12px',
                               color: 'rgba(255,255,255,0.6)' }}>
                    {score > 0 ? score.toFixed(3) : '—'}
                  </td>
                  <td style={{ padding: '12px', fontWeight: 700,
                               color: profit > 0 ? '#10b981' : '#e74c3c' }}>
                    {profit > 0 ? '+' : ''}{profit.toLocaleString()} eur
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </div>
  )
}