import { useState } from 'react'
import Overview from './pages/Overview'
import Segments from './pages/Segments'
import Scoring from './pages/Scoring'
import Decision from './pages/Decision'

const PAGES = {
  Overview,
  Segments,
  Scoring,
  Decision,
}

export default function App() {
  const [page, setPage] = useState('Overview')
  const Page = PAGES[page]
  return (
    <div className="min-h-screen flex">
      <nav className="w-56 bg-gray-900 border-r border-gray-800 p-6 flex flex-col gap-2">
        <div className="text-xs font-semibold text-gray-500 uppercase tracking-widest mb-4">
          Campaign ML
        </div>
        {Object.keys(PAGES).map(p => (
          <button key={p} onClick={() => setPage(p)}
            className={`text-left px-3 py-2 rounded-lg text-sm font-medium transition-colors
              ${page === p
                ? 'bg-brand-500 text-white'
                : 'text-gray-400 hover:text-white hover:bg-gray-800'}`}>
            {p}
          </button>
        ))}
      </nav>
      <main className="flex-1 p-8 overflow-auto">
        <Page />
      </main>
    </div>
  )
}
