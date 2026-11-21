import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {
  Activity,
  Brain,
  Dna,
  Network,
  FileSearch,
  Microscope,
  ShieldCheck,
  LoaderCircle,
  AlertCircle,
  CheckCircle2,
} from 'lucide-react'

import api from '../services/api'
import ProcessingStatus from '../components/ProcessingStatus'
import ReportSummary from '../components/ReportSummary'
import './AnalysisPage.css'

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
    let timeoutId

    const run = async () => {
      try {
        // Trigger analysis
        await api.post(`/analysis/${reportId}`)

        setSteps((s) => ({
          ...s,
          entity_extraction: 'completed',
          disease_identification: 'processing',
        }))

        // Get summary
        const sumRes = await api.get(`/analysis/${reportId}/summary`)

        setSteps((s) => ({
          ...s,
          disease_identification: 'completed',
          disease_normalization: 'completed',
        }))

        setSummary(sumRes.data)

        // Navigate to results
        timeoutId = setTimeout(() => {
          navigate(`/results/${reportId}`)
        }, 2500)

      } catch (e) {
        setError(
          e.response?.data?.detail || 'Analysis failed. Please try again.'
        )
      }
    }

    run()

    return () => {
      if (timeoutId) clearTimeout(timeoutId)
    }
  }, [reportId, navigate])

  const pipeline = [
    {
      icon: FileSearch,
      title: 'Document Processing',
      description: 'Reading and processing uploaded research document',
    },
    {
      icon: Activity,
      title: 'Text Extraction',
      description: 'Extracting relevant biomedical information',
    },
    {
      icon: Dna,
      title: 'Entity Extraction',
      description: 'Identifying genes, proteins and biological entities',
    },
    {
      icon: Brain,
      title: 'Disease Identification',
      description: 'Detecting the primary disease context',
    },
    {
      icon: Network,
      title: 'Disease Normalization',
      description: 'Mapping disease entities to standardized concepts',
    },
  ]

  const completedCount = Object.values(steps).filter(
    (status) => status === 'completed'
  ).length

  const progress = (completedCount / pipeline.length) * 100

  return (
    <div className="analysis-page">

      {/* Background decoration */}
      <div className="analysis-background">
        <div className="analysis-orb orb-one" />
        <div className="analysis-orb orb-two" />
      </div>

      <div className="analysis-container">

        {/* Top header */}
        <div className="analysis-topbar">
          <div className="analysis-brand">
            <div className="analysis-brand-icon">
              <Microscope size={22} />
            </div>
            <div>
              <strong>NeuroSymbolic AI</strong>
              <span>Drug Repurposing Platform</span>
            </div>
          </div>

          <div className="secure-indicator">
            <ShieldCheck size={15} />
            Research Workspace
          </div>
        </div>

        {/* Main heading */}
        <section className="analysis-hero">

          <div className="analysis-status-label">
            <span className="live-dot" />
            {error ? 'PROCESSING INTERRUPTED' : 'AI ANALYSIS IN PROGRESS'}
          </div>

          <div className="analysis-hero-icon">
            {error ? (
              <AlertCircle size={35} />
            ) : (
              <Brain size={35} />
            )}
          </div>

          <h1>
            {error ? 'Analysis Interrupted' : 'Analyzing Your Research'}
          </h1>

          <p>
            {error
              ? 'Something went wrong while processing your document.'
              : 'Our neuro-symbolic pipeline is examining your document to identify biomedical entities and disease associations.'}
          </p>

          <div className="analysis-report-id">
            <span>REPORT ID</span>
            <code>{reportId}</code>
          </div>

        </section>

        {/* Error message */}
        {error && (
          <div className="analysis-error">
            <AlertCircle size={20} />
            <div>
              <strong>Analysis failed</strong>
              <p>{error}</p>
            </div>
          </div>
        )}

        {!error && (
          <>
            {/* Progress card */}
            <section className="analysis-progress-card">

              <div className="progress-card-header">
                <div>
                  <span className="analysis-eyebrow">PROCESSING OVERVIEW</span>
                  <h2>Pipeline Progress</h2>
                </div>

                <div className="progress-percentage">
                  {progress.toFixed(0)}%
                </div>
              </div>

              <div className="analysis-progress-track">
                <div
                  className="analysis-progress-fill"
                  style={{ width: `${progress}%` }}
                />
              </div>

              <div className="progress-card-footer">
                <span>
                  <CheckCircle2 size={15} />
                  {completedCount} of {pipeline.length} stages completed
                </span>

                <span className="processing-indicator">
                  <LoaderCircle size={15} />
                  {summary ? 'Preparing results' : 'Processing'}
                </span>
              </div>

            </section>

            {/* Pipeline stages */}
            <section className="analysis-pipeline-card">

              <div className="pipeline-heading">
                <div>
                  <span className="analysis-eyebrow">NEURO-SYMBOLIC ENGINE</span>
                  <h2>Analysis Pipeline</h2>
                  <p>Real-time status of document processing stages</p>
                </div>

                <div className="pipeline-icon">
                  <Network size={23} />
                </div>
              </div>

              <div className="pipeline-steps">
                {pipeline.map((item, index) => {
                  const Icon = item.icon
                  const status = steps[
                    [
                      'document_processing',
                      'text_extraction',
                      'entity_extraction',
                      'disease_identification',
                      'disease_normalization',
                    ][index]
                  ]

                  return (
                    <div
                      className={`pipeline-step ${status}`}
                      key={item.title}
                    >
                      <div className="pipeline-step-icon">
                        <Icon size={19} />
                      </div>

                      <div className="pipeline-step-content">
                        <h3>{item.title}</h3>
                        <p>{item.description}</p>
                      </div>

                      <div className="pipeline-step-status">
                        {status === 'completed' ? (
                          <>
                            <CheckCircle2 size={17} />
                            <span>Completed</span>
                          </>
                        ) : status === 'processing' ? (
                          <>
                            <LoaderCircle size={17} className="spin-icon" />
                            <span>Processing</span>
                          </>
                        ) : (
                          <span>Pending</span>
                        )}
                      </div>
                    </div>
                  )
                })}
              </div>

            </section>

            {/* Existing processing component */}
            <section className="analysis-existing-status">
              <ProcessingStatus steps={steps} />
            </section>

            {/* Summary */}
            {summary && (
              <section className="analysis-summary-section">
                <div className="summary-ready-label">
                  <CheckCircle2 size={17} />
                  Document analysis completed
                </div>

                <ReportSummary
                  summary={{
                    condition: summary.primary_disease,
                    condition_status: summary.disease_confidence,
                    symptoms: summary.symptoms?.map((s) => s.text) || [],
                    biomarkers: summary.biomarkers?.map((b) => b.text) || [],
                    current_medications:
                      summary.medications?.map((m) => m.text) || [],
                    clinical_findings: summary.genes?.map((g) => g.text) || [],
                  }}
                />

                <div className="analysis-redirect-message">
                  Preparing your drug repurposing results...
                </div>
              </section>
            )}
          </>
        )}

        {/* Footer */}
        <footer className="analysis-footer">
          <span>NEUROSYMBOLIC AI · RESEARCH PROTOTYPE</span>
          <span>Computational research only · Not medical advice</span>
        </footer>

      </div>
    </div>
  )
}