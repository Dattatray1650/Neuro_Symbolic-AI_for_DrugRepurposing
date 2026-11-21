import React from 'react'
import {
  X,
  Target,
  Dna,
  Network,
  Database,
  Award,
  Activity,
  CheckCircle2,
} from 'lucide-react'
import './ResultsComponents.css'

export default function CandidateDetail({ candidate, onClose }) {
  if (!candidate) return null

  const classification = {
    previously_reported: {
      label: 'Previously Reported',
      color: 'green',
    },
    partially_supported: {
      label: 'Partially Supported',
      color: 'blue',
    },
    novel_computational: {
      label: 'Novel Computational',
      color: 'purple',
    },
    insufficient_evidence: {
      label: 'Insufficient Evidence',
      color: 'gray',
    },
  }

  const status =
    classification[candidate.evidence_classification] ||
    classification.insufficient_evidence

  const metrics = [
    {
      label: 'Candidate Score',
      value: candidate.candidate_score,
      icon: Award,
      color: 'blue',
    },
    {
      label: 'Neural Score',
      value: candidate.neural_score,
      icon: Activity,
      color: 'purple',
    },
    {
      label: 'Symbolic Score',
      value: candidate.symbolic_score,
      icon: Network,
      color: 'green',
    },
  ]

  const sections = [
    { title: 'Biological Targets', data: candidate.targets, icon: Target },
    { title: 'Associated Genes', data: candidate.genes, icon: Dna },
    { title: 'Pathways', data: candidate.pathways, icon: Network },
  ]

  return (
    <div className="card candidate-detail">

      <div className="detail-header">
        <div>
          <span className="eyebrow">CANDIDATE PROFILE</span>
          <h2>{candidate.drug_name}</h2>
          <p>Rank #{candidate.rank} · Computational drug candidate</p>
        </div>

        <button className="detail-close" onClick={onClose}>
          <X size={19} />
        </button>
      </div>

      <div className="detail-status-row">
        <span className={`detail-status ${status.color}`}>
          <CheckCircle2 size={14} />
          {status.label}
        </span>
        <span className="detail-rank">RANK #{candidate.rank}</span>
      </div>

      <div className="detail-metrics">
        {metrics.map((metric) => {
          const Icon = metric.icon
          const value = Number(metric.value)

          return (
            <div className="detail-metric" key={metric.label}>
              <div className={`metric-icon ${metric.color}`}>
                <Icon size={19} />
              </div>

              <span className="metric-label">{metric.label}</span>

              <strong>
                {Number.isFinite(value) ? value.toFixed(3) : 'N/A'}
              </strong>

              <div className="metric-track">
                <div
                  className={`metric-progress ${metric.color}`}
                  style={{
                    width: `${Number.isFinite(value) ? Math.min(Math.max(value, 0), 1) * 100 : 0}%`,
                  }}
                />
              </div>
            </div>
          )
        })}
      </div>

      {candidate.explanation && (
        <div className="detail-explanation">
          <h3>Research Explanation</h3>
          <p>{candidate.explanation}</p>
        </div>
      )}

      <div className="detail-section">
        <h3>Biological Associations</h3>

        <div className="association-grid">
          {sections.map((section) => {
            const Icon = section.icon

            return (
              <div className="association-card" key={section.title}>
                <div className="association-heading">
                  <Icon size={17} />
                  <span>{section.title}</span>
                </div>

                <div className="association-tags">
                  {section.data?.length > 0 ? (
                    section.data.map((item, index) => (
                      <span key={index} className="association-tag">
                        {item}
                      </span>
                    ))
                  ) : (
                    <span className="empty-value">No data available</span>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      </div>

      {candidate.sources?.length > 0 && (
        <div className="detail-sources">
          <div className="association-heading">
            <Database size={17} />
            <span>Research Data Sources</span>
          </div>

          <div className="source-list">
            {candidate.sources.map((source, index) => (
              <span key={index}>{source}</span>
            ))}
          </div>
        </div>
      )}

      <div className="detail-disclaimer">
        Computational research findings only. These scores do not establish
        clinical effectiveness or treatment suitability.
      </div>

    </div>
  )
}