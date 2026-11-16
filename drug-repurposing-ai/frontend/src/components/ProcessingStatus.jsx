import React from 'react'

const STEPS = [
  { key: 'document_processing', label: 'Document processed' },
  { key: 'text_extraction', label: 'Text extracted' },
  { key: 'entity_extraction', label: 'Clinical entities extracted' },
  { key: 'disease_identification', label: 'Diagnosis/condition identified' },
  { key: 'disease_normalization', label: 'Disease normalized' },
]

function StatusIcon({ status }) {
  if (status === 'completed') return <span className="step-icon completed">✓</span>
  if (status === 'processing') return <span className="step-icon processing">⟳</span>
  return <span className="step-icon pending">○</span>
}

export default function ProcessingStatus({ steps = {} }) {
  return (
    <div className="card">
      <h3 className="text-lg font-semibold mb-4">Processing Status</h3>
      <div className="space-y-3">
        {STEPS.map(({ key, label }) => (
          <div key={key} className="flex items-center gap-3">
            <StatusIcon status={steps[key] || 'pending'} />
            <span className={`text-sm ${steps[key] === 'completed' ? 'text-gray-900' : 'text-gray-500'}`}>
              {label}
            </span>
          </div>
        ))}
      </div>
    </div>
  )
}
