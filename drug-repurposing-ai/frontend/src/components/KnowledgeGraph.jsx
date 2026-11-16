import React from 'react'

const nodeColors = {
  Drug: '#3b82f6',
  Disease: '#ef4444',
  Gene: '#22c55e',
  Protein: '#a855f7',
  Pathway: '#f59e0b',
}

export default function KnowledgeGraph({ graphData, onNodeClick }) {
  if (!graphData?.nodes?.length) {
    return (
      <div className="card text-center text-gray-500">
        <h3 className="text-lg font-semibold mb-2">Knowledge Graph</h3>
        <p>Interactive graph visualization will appear here when data is available.</p>
        <p className="text-xs mt-2 text-gray-400">
          (react-force-graph-2d will render the graph in later phases)
        </p>
      </div>
    )
  }

  return (
    <div className="card" style={{ padding: 0 }}>
      <div className="p-4 border-b">
        <h3 className="text-lg font-semibold">Knowledge Graph</h3>
        <div className="flex gap-4 mt-2">
          {Object.entries(nodeColors).map(([type, color]) => (
            <div key={type} className="flex items-center gap-1">
              <div style={{ width: 12, height: 12, borderRadius: '50%', background: color }} />
              <span className="text-xs text-gray-600">{type}</span>
            </div>
          ))}
        </div>
      </div>
      <div style={{ height: 500, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <p className="text-gray-400">Graph visualization placeholder — will be connected in Phase 9</p>
      </div>
    </div>
  )
}
