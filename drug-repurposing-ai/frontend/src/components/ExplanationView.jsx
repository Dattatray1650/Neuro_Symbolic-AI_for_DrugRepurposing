import React from 'react'

export default function ExplanationView({ candidate }) {
  if (!candidate) return null

  const items = (candidate.evidence_paths || []).map((path) => ({
    text: path.path.join(' → '),
    rule: path.rule,
    weight: path.weight,
  }))

  return (
    <div className="card">
      <h3 className="text-lg font-semibold mb-4">Why This Candidate?</h3>
      <p className="text-sm text-gray-600 mb-4">
        {candidate.drug_name} was ranked #{candidate.rank} because:
      </p>

      <div className="space-y-3">
        {items.map((item, i) => (
          <div key={i} className="flex gap-2" style={{ alignItems: 'flex-start' }}>
            <span className="text-green-500 flex-shrink-0">✓</span>
            <div>
              <p className="text-sm text-gray-700">{item.text}</p>
              <p className="text-xs text-gray-400">Rule: {item.rule} (weight: {item.weight})</p>
            </div>
          </div>
        ))}

        {candidate.neural_score > 0 && (
          <div className="flex gap-2" style={{ alignItems: 'flex-start' }}>
            <span className="text-blue-500 flex-shrink-0">✓</span>
            <p className="text-sm text-gray-700">
              The neural model assigns a high embedding similarity (score: {candidate.neural_score.toFixed(3)})
            </p>
          </div>
        )}

        <div className="flex gap-2" style={{ alignItems: 'flex-start' }}>
          <span className="text-purple-500 flex-shrink-0">✓</span>
          <p className="text-sm text-gray-700">
            {items.length} distinct knowledge-graph path(s) support this candidate
          </p>
        </div>
      </div>
    </div>
  )
}
