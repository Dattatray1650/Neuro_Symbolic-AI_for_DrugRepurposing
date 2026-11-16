import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import api from '../services/api'
import ProcessingStatus from '../components/ProcessingStatus'
import ReportSummary from '../components/ReportSummary'

export default function AnalysisPage() {
  const { reportId } = useParams()
  const navigate = useNavigate()
  const [steps, setSteps] = useState({
    document_processing: 'completed',
    text_extraction: 'completed',
    entity_extraction: 'processing',
    disease_identification: 'pending',
    disease_normalization: 'pending',
  })
  const [summary, setSummary] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    const run = async () => {
      try {
        // Trigger analysis
        await api.post(`/analysis/${reportId}`)
        setSteps(s => ({...s, entity_extraction:'completed', disease_identification:'processing'}))

        // Get summary
        const sumRes = await api.get(`/analysis/${reportId}/summary`)
        setSteps(s => ({...s, disease_identification:'completed', disease_normalization:'completed'}))
        setSummary(sumRes.data)

        // Navigate to results after 1.5s
        setTimeout(() => navigate(`/results/${reportId}`), 1500)
      } catch (e) {
        setError(e.response?.data?.detail || 'Analysis failed.')
      }
    }
    run()
  }, [reportId])

  return (
    <div style={{maxWidth:'600px', margin:'0 auto'}}>
      <h2 className="text-2xl font-bold text-gray-900 mb-2">Analyzing Report</h2>
      <p className="text-sm text-gray-500 mb-6">Running NLP pipeline and knowledge graph lookup...</p>

      {error && (
        <div className="card bg-red-50 mb-4" style={{borderColor:'#fca5a5'}}>
          <p className="text-red-600 text-sm">{error}</p>
        </div>
      )}

      <div className="space-y-4">
        <ProcessingStatus steps={steps} />
        {summary && <ReportSummary summary={{
          condition: summary.primary_disease,
          condition_status: summary.disease_confidence,
          symptoms: summary.symptoms?.map(s => s.text) || [],
          biomarkers: summary.biomarkers?.map(b => b.text) || [],
          current_medications: summary.medications?.map(m => m.text) || [],
          clinical_findings: summary.genes?.map(g => g.text) || [],
        }} />}
      </div>
    </div>
  )
}
