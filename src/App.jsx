import { useState } from 'react'
import Overview from './pages/Overview'
import Segments from './pages/Segments'
import Scoring from './pages/Scoring'
import Decision from './pages/Decision'

const PAGES = { Overview, Segments, Scoring, Decision }

const NAV = [
  { key: 'Overview', label: 'Vue generale',    icon: '▦' },
  { key: 'Segments', label: 'Segments clients', icon: '◈' },
  { key: 'Scoring',  label: 'Scoring ML',       icon: '◎' },
  { key: 'Decision', label: 'Decision ROI',     icon: '◆' },
]

export default function App() {
  const [page, setPage] = useState('Overview')
  const Page = PAGES[page]

  return (
    <div style={{
      display: 'flex', minHeight: '100vh',
      background: '#080C14', color: '#e2e8f0',
      fontFamily: "'Inter', sans-serif",
      flexDirection: 'column'
    }}>

      {/* Navigation mobile — visible uniquement sur petit ecran */}
      <div style={{
        display: 'flex',
        background: '#0d1526',
        borderBottom: '1px solid rgba(79,110,247,0.15)',
        padding: '12px 16px', gap: '8px',
        position: 'sticky', top: 0, zIndex: 100,
        overflowX: 'auto'
      }}
        className="mobile-nav">
        <div style={{
          fontSize: '11px', color: '#4f6ef7', fontWeight: 700,
          letterSpacing: '2px', alignSelf: 'center',
          whiteSpace: 'nowrap', marginRight: '8px'
        }}>CAMPAIGN ML</div>
        {NAV.map(({ key, label }) => {
          const active = page === key
          return (
            <button key={key} onClick={() => setPage(key)} style={{
              padding: '8px 14px', borderRadius: '20px', border: 'none',
              cursor: 'pointer', whiteSpace: 'nowrap',
              background: active ? '#4f6ef7' : 'rgba(255,255,255,0.06)',
              color: active ? '#fff' : 'rgba(255,255,255,0.5)',
              fontSize: '12px', fontWeight: active ? 600 : 400,
            }}>{label}</button>
          )
        })}
      </div>

      <div style={{ display: 'flex', flex: 1 }}>

        {/* Sidebar desktop */}
        <aside className="sidebar" style={{
          width: '220px',
          background: 'linear-gradient(180deg, #0d1526 0%, #0a1020 100%)',
          borderRight: '1px solid rgba(79,110,247,0.15)',
          display: 'flex', flexDirection: 'column', flexShrink: 0
        }}>
          <div style={{
            padding: '28px 24px 24px',
            borderBottom: '1px solid rgba(79,110,247,0.1)'
          }}>
            <div style={{
              fontSize: '10px', fontWeight: 700, letterSpacing: '3px',
              color: '#4f6ef7', textTransform: 'uppercase', marginBottom: '4px'
            }}>Campaign ML</div>
            <div style={{
              fontSize: '13px', color: 'rgba(255,255,255,0.4)',
              fontWeight: 400, lineHeight: 1.4
            }}>Intelligence Decisionnelle</div>
          </div>

          <nav style={{ padding: '16px 12px', flex: 1 }}>
            {NAV.map(({ key, label, icon }) => {
              const active = page === key
              return (
                <button key={key} onClick={() => setPage(key)} style={{
                  width: '100%', display: 'flex', alignItems: 'center',
                  gap: '10px', padding: '11px 14px', borderRadius: '8px',
                  border: 'none', cursor: 'pointer', marginBottom: '4px',
                  background: active
                    ? 'linear-gradient(90deg, rgba(79,110,247,0.25) 0%, rgba(79,110,247,0.08) 100%)'
                    : 'transparent',
                  borderLeft: active ? '2px solid #4f6ef7' : '2px solid transparent',
                  color: active ? '#7b9ffb' : 'rgba(255,255,255,0.4)',
                  fontSize: '13px', fontWeight: active ? 600 : 400,
                  textAlign: 'left', transition: 'all 0.15s ease',
                }}>
                  <span style={{ fontSize: '14px', opacity: active ? 1 : 0.5 }}>
                    {icon}
                  </span>
                  {label}
                </button>
              )
            })}
          </nav>

          <div style={{
            padding: '16px 24px',
            borderTop: '1px solid rgba(79,110,247,0.1)',
            fontSize: '10px', color: 'rgba(255,255,255,0.2)',
            letterSpacing: '0.5px'
          }}>v1.0.0 — 2024</div>
        </aside>

        {/* Main content */}
        <main style={{ flex: 1, overflowY: 'auto', background: '#080C14' }}>
          <Page />
        </main>
      </div>
    </div>
  )
}