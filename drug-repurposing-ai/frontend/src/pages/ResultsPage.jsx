import './ResultsPage.css'
import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import api from '../services/api'
import CandidateResults from '../components/CandidateResults'
import CandidateDetail from '../components/CandidateDetail'
import ExplanationView from '../components/ExplanationView'
import KnowledgeGraph from '../components/KnowledgeGraph'

export default function ResultsPage() {
  const { reportId } = useParams()
  const [results, setResults] = useState(null)
  const [graphData, setGraphData] = useState(null)
  const [selected, setSelected] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const load = async () => {
      try {
        const [resR, graphR] = await Promise.all([
  api.get(`/results/${reportId}`),
  api.get(`/results/${reportId}/graph`),
])

console.log('RESULTS API RESPONSE:', resR.data)
console.log('CANDIDATES:', resR.data.candidates)

setResults(resR.data)
setGraphData(graphR.data)

if (resR.data.candidates?.length > 0) {
  setSelected(resR.data.candidates[0])
}
        if (resR.data.candidates?.length > 0) setSelected(resR.data.candidates[0])
      } catch(e) {
        setError(e.response?.data?.detail || 'Failed to load results.')
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [reportId])

  if (loading) return (
    <div className="text-center py-12">
      <p className="text-gray-500">Loading results...</p>
    </div>
  )
  if (error) return (
    <div className="card bg-red-50"><p className="text-red-600">{error}</p></div>
  )

  return (
    <div className="results-page">
      {/* Header */}
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Drug Repurposing Results</h2>
        {results?.disease && (
          <p className="text-gray-600 mt-1">
            Condition: <strong>{results.disease}</strong>
            {' '}
            <span className="badge" style={{background:'#dcfce7',color:'#166534'}}>
              {results.disease_confidence}
            </span>
          </p>
        )}
        <p className="text-xs text-gray-400 mt-1">
          {results?.total_candidates} candidates | Fusion: Neural×0.6 + Symbolic×0.4
        </p>
      </div>

      {/* Demo banner */}
      <div className="card mb-6" style={{background:'#fefce8',border:'1px solid #fde68a',padding:'0.75rem 1rem'}}>
        <p className="text-xs" style={{color:'#854d0e'}}>
          ⚠ <strong>DEMO / RESEARCH DATA</strong> — Candidates sourced from curated ChEMBL, DisGeNET,
          Open Targets subset. This is a computational research prototype, not medical advice.
        </p>
      </div>

      <div className="grid gap-6" style={{gridTemplateColumns:'1fr 1fr'}}>
        {/* Left: Candidate list */}
        <CandidateResults
          candidates={results?.candidates || []}
          onSelect={setSelected}
        />

        {/* Right: Detail + Explanation */}
        <div className="space-y-4">
          {selected && <CandidateDetail candidate={selected} onClose={() => setSelected(null)} />}
          {selected && <ExplanationView candidate={selected} />}
        </div>
      </div>

      {/* Knowledge Graph */}
      <div className="mt-6">
        <KnowledgeGraph graphData={graphData} />
      </div>
    </div>
  )
}
