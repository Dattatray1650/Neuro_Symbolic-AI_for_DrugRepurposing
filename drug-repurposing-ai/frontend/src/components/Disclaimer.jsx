import React from 'react'

export default function Disclaimer() {
  return (
    <div className="disclaimer-banner">
      <div className="container flex gap-2 items-center" style={{ alignItems: 'flex-start' }}>
        <span style={{ fontSize: '1.1rem', marginTop: '1px' }}>⚠️</span>
        <p>
          <strong>Research Disclaimer:</strong> This system generates computational
          drug-repurposing hypotheses for research purposes only. It does not provide
          medical advice, diagnosis, or treatment recommendations. Candidate drugs
          require independent experimental, clinical, and regulatory validation.
        </p>
      </div>
    </div>
  )
}
