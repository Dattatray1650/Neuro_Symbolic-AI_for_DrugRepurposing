import React from 'react'
import { Brain, GitBranch, CheckCircle2, Info } from 'lucide-react'
import './ResultsComponents.css'

export default function ExplanationView({ candidate }) {
  if (!candidate) return null

  const items = (candidate.evidence_paths || []).map((path) => ({
    text: Array.isArray(path.path) ? path.path.join(' → ') : 'Evidence path unavailable',
    rule: path.rule || 'Knowledge graph rule',
    weight: path.weight,
  }))

  return (
    <div className="card explanation-card">

      <div className="explanation-header">
        <div>
          <span className="eyebrow">AI REASONING</span>
          <h3>Why This Candidate?</h3>
        </div>
        <div className="explanation-icon">
          <Brain size={22} />
        </div>
      </div>

      <p className="explanation-intro">
        <strong>{candidate.drug_name}</strong> was ranked #{candidate.rank}
        based on the following computational evidence.
      </p>

      <div className="explanation-items">

        {items.map((item, i) => (
          <div className="explanation-item" key={i}>
            <div className="explanation-check">
              <CheckCircle2 size={17} />
            </div>

            <div className="explanation-content">
              <p className="explanation-path">{item.text}</p>
              <span className="explanation-meta">
                Rule: {item.rule}
                {item.weight != null && ` · Weight: ${item.weight}`}
              </span>
            </div>
          </div>
        ))}

        {candidate.neural_score > 0 && (
          <div className="explanation-item">
            <div className="explanation-check neural">
              <Brain size={17} />
            </div>

            <div className="explanation-content">
              <p className="explanation-path">
                Neural model similarity score
              </p>
              <span className="explanation-meta">
                Score: {candidate.neural_score.toFixed(3)}
              </span>
            </div>
          </div>
        )}

        <div className="explanation-item">
          <div className="explanation-check graph">
            <GitBranch size={17} />
          </div>

          <div className="explanation-content">
            <p className="explanation-path">
              {items.length} knowledge-graph evidence path(s) identified
            </p>
            <span className="explanation-meta">
              Based on available computational research data
            </span>
          </div>
        </div>

      </div>

      <div className="explanation-note">
        <Info size={16} />
        <p>
          These explanations represent computational evidence, not proof of
          clinical effectiveness or a medical recommendation.
        </p>
      </div>

    </div>
  )
}