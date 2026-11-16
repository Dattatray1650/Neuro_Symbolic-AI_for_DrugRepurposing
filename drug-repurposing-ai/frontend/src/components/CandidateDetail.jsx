import React from 'react'

export default function CandidateDetail({ candidate, onClose }) {
  if (!candidate) return null

  const classificationColors = {
    previously_reported: { bg: '#dcfce7', color: '#166534' },
    partially_supported: { bg: '#dbeafe', color: '#1e40af' },
    novel_computational: { bg: '#f3e8ff', color: '#6b21a8' },
    insufficient_evidence: { bg: '#f3f4f6', color: '#374151' },
  }

  const cls = classificationColors[candidate.evidence_classification] || classificationColors.insufficient_evidence

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-bold text-gray-900">{candidate.drug_name}</h3>
        <button onClick={onClose} style={{ background: 'none', border: 'none', cursor: 'pointer', fontSize: '1.2rem' }}>✕</button>
      </div>

      {/* Scores */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        <div className="text-center p-3 bg-gray-50 rounded-lg">
          <p className="text-2xl font-bold text-gray-900">{candidate.candidate_score.toFixed(3)}</p>
          <p className="text-xs text-gray-500">Candidate Score</p>
        </div>
        <div className="text-center p-3 bg-blue-50 rounded-lg">
          <p className="text-2xl font-bold text-blue-700">{candidate.neural_score.toFixed(3)}</p>
          <p className="text-xs text-gray-500">Neural Score</p>
        </div>
        <div className="text-center p-3 bg-green-50 rounded-lg">
          <p className="text-2xl font-bold text-green-700">{candidate.symbolic_score.toFixed(3)}</p>
          <p className="text-xs text-gray-500">Symbolic Score</p>
        </div>
      </div>

      {/* Classification */}
      <div className="mb-4">
        <span className="badge" style={{ background: cls.bg, color: cls.color }}>
          {candidate.evidence_classification?.replace(/_/g, ' ')}
        </span>
      </div>

      {/* Explanation */}
      {candidate.explanation && (
        <div className="mb-6">
          <h4 className="font-semibold text-gray-700 mb-2">🎯 Why This Candidate?</h4>
          <div className="bg-gray-50 p-4 rounded-lg text-sm text-gray-700 whitespace-pre-line">
            {candidate.explanation}
          </div>
        </div>
      )}

      {/* Evidence Paths */}
      {candidate.evidence_paths?.length > 0 && (
        <div className="mb-6">
          <h4 className="font-semibold text-gray-700 mb-2">🔀 Reasoning Paths</h4>
          <div className="space-y-2">
            {candidate.evidence_paths.map((path, i) => (
              <div key={i} className="bg-gray-50 p-3 rounded-lg">
                <p className="text-xs text-gray-500 mb-1 font-medium">{path.rule}</p>
                <p className="text-sm text-gray-700">{path.path.join(' → ')}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Targets, Genes, Pathways */}
      <div className="grid grid-cols-3 gap-4">
        {candidate.targets?.length > 0 && (
          <div>
            <h5 className="text-xs font-medium text-gray-500 mb-1">Targets</h5>
            <div className="flex flex-wrap gap-1">
              {candidate.targets.map((t, i) => (
                <span key={i} className="badge" style={{ background: '#eff6ff', color: '#1d4ed8' }}>{t}</span>
              ))}
            </div>
          </div>
        )}
        {candidate.genes?.length > 0 && (
          <div>
            <h5 className="text-xs font-medium text-gray-500 mb-1">Genes</h5>
            <div className="flex flex-wrap gap-1">
              {candidate.genes.map((g, i) => (
                <span key={i} className="badge" style={{ background: '#f0fdf4', color: '#15803d' }}>{g}</span>
              ))}
            </div>
          </div>
        )}
        {candidate.pathways?.length > 0 && (
          <div>
            <h5 className="text-xs font-medium text-gray-500 mb-1">Pathways</h5>
            <div className="flex flex-wrap gap-1">
              {candidate.pathways.map((p, i) => (
                <span key={i} className="badge" style={{ background: '#faf5ff', color: '#7e22ce' }}>{p}</span>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Sources */}
      {candidate.sources?.length > 0 && (
        <div className="mt-4" style={{ paddingTop: '1rem', borderTop: '1px solid #f1f5f9' }}>
          <h5 className="text-xs font-medium text-gray-500 mb-1">Data Sources</h5>
          <p className="text-xs text-gray-600">{candidate.sources.join(', ')}</p>
        </div>
      )}
    </div>
  )
}
