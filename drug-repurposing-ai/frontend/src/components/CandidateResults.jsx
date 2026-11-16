import React from 'react'

export default function CandidateResults({ candidates = [], onSelect }) {
  if (candidates.length === 0) {
    return (
      <div className="card text-center text-gray-500">
        No candidates generated yet.
      </div>
    )
  }

  return (
    <div className="card" style={{ padding: 0 }}>
      <div className="p-4 border-b">
        <h3 className="text-lg font-semibold">Potential Drug-Repurposing Candidates</h3>
        <p className="text-sm text-gray-500 mt-1">
          Identified from computational evidence — not medical recommendations
        </p>
      </div>

      <div>
        {candidates.map((candidate) => (
          <div
            key={candidate.drug_id}
            className="candidate-item"
            onClick={() => onSelect(candidate)}
          >
            <div className="flex items-center justify-between mb-2">
              <div>
                <span className="text-sm font-medium text-gray-400 mr-2">
                  #{candidate.rank}
                </span>
                <span className="font-semibold text-gray-900">
                  {candidate.drug_name}
                </span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-sm font-medium text-gray-700">
                  Score: {candidate.candidate_score.toFixed(3)}
                </span>
                <span>→</span>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4 mt-2">
              <div>
                <span className="text-xs text-gray-500">Neural: {candidate.neural_score.toFixed(3)}</span>
                <div className="score-bar">
                  <div className="score-bar-fill blue" style={{ width: `${candidate.neural_score * 100}%` }} />
                </div>
              </div>
              <div>
                <span className="text-xs text-gray-500">Symbolic: {candidate.symbolic_score.toFixed(3)}</span>
                <div className="score-bar">
                  <div className="score-bar-fill green" style={{ width: `${candidate.symbolic_score * 100}%` }} />
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
