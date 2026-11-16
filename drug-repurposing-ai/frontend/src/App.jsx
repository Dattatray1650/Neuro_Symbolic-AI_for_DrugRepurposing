import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import HomePage from './pages/HomePage'
import AnalysisPage from './pages/AnalysisPage'
import ResultsPage from './pages/ResultsPage'
import Disclaimer from './components/Disclaimer'

function App() {
  return (
    <Router>
      <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
        {/* Header */}
        <header className="header">
          <div className="container">
            <h1>🧬 Drug Repurposing AI</h1>
            <p>Neuro-Symbolic AI for Explainable Drug Repurposing from Medical Reports</p>
          </div>
        </header>

        {/* Disclaimer Banner */}
        <Disclaimer />

        {/* Main Content */}
        <main style={{ flex: 1 }} className="container py-8">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/analysis/:reportId" element={<AnalysisPage />} />
            <Route path="/results/:reportId" element={<ResultsPage />} />
          </Routes>
        </main>

        {/* Footer */}
        <footer className="footer">
          <div className="container">
            Research Prototype — Not for clinical use
          </div>
        </footer>
      </div>
    </Router>
  )
}

export default App
