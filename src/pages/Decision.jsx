import kpis from '../data/kpis.json'

const strategies = [
  { name: 'Tous les clients',       contacted: 443, converted: 67,
    profit: 2270,  roi: 51,   precision: 0.15, recall: 1.00,
    recommended: false },
  { name: 'Seuil defaut (0.50)',    contacted: 37,  converted: 28,
    profit: 2430,  roi: 657,  precision: 0.76, recall: 0.42,
    recommended: false },
  { name: 'Seuil optimal (0.07)',   contacted: 158, converted: 63,
    profit: 4720,  roi: 299,  precision: 0.40, recall: 0.94,
    recommended: true },
  { name: 'Top 20% scores',         contacted: 89,  converted: 44,
    profit: 3510,  roi: 394,  precision: 0.49, recall: 0.66,
    recommended: false },
  { name: 'Premium Engages seul',   contacted: 38,  converted: 21,
    profit: 1720,  roi: 453,  precision: 0.55, recall: 0.31,
    recommended: false },
]

const rules = [
  { rule: 'Score de probabilite',  value: '>= 0.07',       color: '#4f6ef7' },
  { rule: 'Segment prioritaire',   value: 'Premium Engages', color: '#10b981' },
  { rule: 'Recency',               value: '< 70 jours',    color: '#f59e0b' },
  { rule: 'Segment a exclure',     value: 'Petits Budgets', color: '#e74c3c' },
]

export default function Decision() {
  const best = strategies.find(s => s.recommended)

  return (
    <div style={{ padding: 'clamp(16px, 4vw, 32px)' }}>

      {/* Header */}
      <div style={{ marginBottom: '28px' }}>
        <div style={{ fontSize: '11px', color: '#4f6ef7', fontWeight: 600,
                      letterSpacing: '2px', textTransform: 'uppercase',
                      marginBottom: '8px' }}>Optimisation marketing</div>
        <h1 style={{ fontSize: 'clamp(20px, 4vw, 28px)', fontWeight: 700,
                     color: '#fff', margin: 0 }}>Decision ROI</h1>
        <p style={{ fontSize: '14px', color: 'rgba(255,255,255,0.4)',
                    marginTop: '6px' }}>
          Strategie de ciblage optimale et extrapolation business
        </p>
      </div>

      {/* Strategie recommandee */}
      <div style={{
        background: 'linear-gradient(135deg, rgba(16,185,129,0.1) 0%, rgba(16,185,129,0.05) 100%)',
        border: '1px solid rgba(16,185,129,0.3)',
        borderRadius: '12px', padding: '24px', marginBottom: '20px'
      }}>
        <div style={{ fontSize: '11px', color: '#10b981', fontWeight: 600,
                      letterSpacing: '2px', textTransform: 'uppercase',
                      marginBottom: '16px' }}>Strategie recommandee</div>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(120px, 1fr))',
          gap: '16px'
        }}>
          {[
            { val: best.name,                 label: 'Strategie' },
            { val: best.contacted,            label: 'Clients a contacter' },
            { val: best.converted,            label: 'Conversions attendues' },
            { val: `${best.profit.toLocaleString()} eur`, label: 'Profit net' },
            { val: `${best.roi}%`,            label: 'ROI' },
            { val: best.precision,            label: 'Precision' },
          ].map((item, i) => (
            <div key={i} style={{ textAlign: 'center' }}>
              <div style={{ fontSize: i === 0 ? '14px' : '22px',
                            fontWeight: 700, color: '#10b981',
                            lineHeight: 1.2 }}>{item.val}</div>
              <div style={{ fontSize: '10px',
                            color: 'rgba(255,255,255,0.4)',
                            marginTop: '4px', textTransform: 'uppercase',
                            letterSpacing: '0.5px' }}>{item.label}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Comparaison strategies */}
      <div style={{
        background: 'linear-gradient(135deg, #0d1526 0%, #111827 100%)',
        border: '1px solid rgba(79,110,247,0.15)',
        borderRadius: '12px', padding: '24px',
        marginBottom: '20px', overflowX: 'auto'
      }}>
        <div style={{ fontSize: '11px', color: '#4f6ef7', fontWeight: 600,
                      letterSpacing: '2px', textTransform: 'uppercase',
                      marginBottom: '16px' }}>Comparaison des strategies</div>

        <table style={{ width: '100%', borderCollapse: 'collapse',
                        fontSize: '13px', minWidth: '560px' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.08)' }}>
              {['Strategie','Contactes','Convertis','Profit','ROI','Precision','Recall'].map(h => (
                <th key={h} style={{ padding: '10px 12px', textAlign: 'left',
                                     fontSize: '10px', fontWeight: 600,
                                     color: 'rgba(255,255,255,0.35)',
                                     textTransform: 'uppercase',
                                     letterSpacing: '1px' }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {strategies.map((s, i) => (
              <tr key={i} style={{
                borderBottom: '1px solid rgba(255,255,255,0.04)',
                background: s.recommended ? 'rgba(16,185,129,0.06)' : 'transparent'
              }}>
                <td style={{ padding: '12px', color: '#fff', fontWeight: 600 }}>
                  {s.recommended && (
                    <span style={{ color: '#10b981', marginRight: '6px' }}>*</span>
                  )}
                  {s.name}
                </td>
                <td style={{ padding: '12px',
                             color: 'rgba(255,255,255,0.6)' }}>{s.contacted}</td>
                <td style={{ padding: '12px',
                             color: 'rgba(255,255,255,0.6)' }}>{s.converted}</td>
                <td style={{ padding: '12px', fontWeight: 700,
                             color: '#10b981' }}>{s.profit.toLocaleString()} eur</td>
                <td style={{ padding: '12px', fontWeight: 700,
                             color: '#4f6ef7' }}>{s.roi}%</td>
                <td style={{ padding: '12px',
                             color: 'rgba(255,255,255,0.6)' }}>{s.precision}</td>
                <td style={{ padding: '12px',
                             color: 'rgba(255,255,255,0.6)' }}>{s.recall}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Regles + Extrapolation */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
        gap: '16px'
      }}>

        {/* Regles */}
        <div style={{
          background: 'linear-gradient(135deg, #0d1526 0%, #111827 100%)',
          border: '1px solid rgba(79,110,247,0.15)',
          borderRadius: '12px', padding: '24px'
        }}>
          <div style={{ fontSize: '11px', color: '#4f6ef7', fontWeight: 600,
                        letterSpacing: '2px', textTransform: 'uppercase',
                        marginBottom: '16px' }}>Regles de ciblage</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {rules.map((r, i) => (
              <div key={i} style={{
                display: 'flex', justifyContent: 'space-between',
                alignItems: 'center', padding: '10px 14px',
                background: 'rgba(255,255,255,0.04)', borderRadius: '8px',
                borderLeft: `3px solid ${r.color}`
              }}>
                <span style={{ fontSize: '12px',
                               color: 'rgba(255,255,255,0.5)' }}>{r.rule}</span>
                <span style={{ fontSize: '12px', fontWeight: 700,
                               color: r.color }}>{r.value}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Extrapolation */}
        <div style={{
          background: 'linear-gradient(135deg, #0d1526 0%, #111827 100%)',
          border: '1px solid rgba(79,110,247,0.15)',
          borderRadius: '12px', padding: '24px'
        }}>
          <div style={{ fontSize: '11px', color: '#4f6ef7', fontWeight: 600,
                        letterSpacing: '2px', textTransform: 'uppercase',
                        marginBottom: '16px' }}>Extrapolation base complete</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {[
              { label: 'Base totale clients',  val: '2 212',       color: '#fff' },
              { label: 'Clients a cibler',     val: '788',         color: '#4f6ef7' },
              { label: 'Conversions attendues',val: '314',         color: '#4f6ef7' },
              { label: 'Budget campagne',      val: '7 880 eur',   color: '#f59e0b' },
              { label: 'Profit net attendu',   val: '23 568 eur',  color: '#10b981' },
              { label: 'ROI',                  val: '299%',        color: '#10b981' },
            ].map((item, i) => (
              <div key={i} style={{
                display: 'flex', justifyContent: 'space-between',
                alignItems: 'center',
                paddingBottom: '10px',
                borderBottom: i < 5 ? '1px solid rgba(255,255,255,0.05)' : 'none'
              }}>
                <span style={{ fontSize: '12px',
                               color: 'rgba(255,255,255,0.4)' }}>{item.label}</span>
                <span style={{ fontSize: '15px', fontWeight: 700,
                               color: item.color }}>{item.val}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}