import React from 'react'
import './ResultsComponents.css'

const nodeColors = {
  Drug: '#3b82f6',
  Disease: '#ef4444',
  Gene: '#22c55e',
  Protein: '#a855f7',
  Pathway: '#f59e0b',
}

export default function KnowledgeGraph({ graphData, onNodeClick }) {
  const nodes = graphData?.nodes || []

  if (!nodes.length) {
    return (
      <div className="card knowledge-graph">
        <div className="graph-header">
          <div>
            <span className="eyebrow">BIOMEDICAL NETWORK</span>
            <h3>Knowledge Graph</h3>
            <p>Explore relationships between biomedical entities.</p>
          </div>
          <span className="graph-status">Awaiting graph data</span>
        </div>

        <div className="graph-empty">
          <div className="graph-empty-icon">◎</div>
          <h4>No graph data available</h4>
          <p>
            The graph will appear when biomedical relationship data
            is returned by the backend.
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="card knowledge-graph">
      <div className="graph-header">
        <div>
          <span className="eyebrow">BIOMEDICAL NETWORK</span>
          <h3>Knowledge Graph</h3>
          <p>Biomedical entities identified in this analysis.</p>
        </div>

        <span className="graph-count">
          {nodes.length} Nodes
        </span>
      </div>

      <div className="graph-legend">
        {Object.entries(nodeColors).map(([type, color]) => (
          <div className="legend-item" key={type}>
            <span
              className="legend-dot"
              style={{ background: color }}
            />
            {type}
          </div>
        ))}
      </div>

      <div className="graph-node-list">
        {nodes.map((node, index) => {
          const type = node.type || node.label || 'Drug'
          const color = nodeColors[type] || '#64748b'

          return (
            <button
              key={node.id || index}
              className="graph-node"
              onClick={() => onNodeClick?.(node)}
            >
              <span
                className="legend-dot"
                style={{ background: color }}
              />
              <span>{node.name || node.id || 'Unknown entity'}</span>
              <small>{type}</small>
            </button>
          )
        })}
      </div>

      <div className="graph-note">
        Entity listing only — this is not an interactive network visualization.
      </div>
    </div>
  )
}