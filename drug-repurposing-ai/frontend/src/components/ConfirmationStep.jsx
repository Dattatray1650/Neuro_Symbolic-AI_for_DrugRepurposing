import React from 'react'

export default function ConfirmationStep({ diagnosis, status, onContinue }) {
  return (
    <div className="card">
      <h3 className="text-lg font-semibold mb-4">Confirm Identified Condition</h3>

      {status === 'confirmed' ? (
        <div>
          <p className="text-gray-600 mb-2">We identified the following condition from the report:</p>
          <p className="text-xl font-semibold text-gray-900 mb-4">{diagnosis}</p>
        </div>
      ) : (
        <div className="flex gap-3 mb-4" style={{ alignItems: 'flex-start' }}>
          <span style={{ color: '#f59e0b', fontSize: '1.2rem' }}>⚠️</span>
          <div>
            <p className="text-gray-600">No confirmed diagnosis was explicitly identified.</p>
            {diagnosis && (
              <p className="text-gray-700 mt-1">
                Possible condition: <span className="font-medium">{diagnosis}</span>
              </p>
            )}
          </div>
        </div>
      )}

      <button onClick={onContinue} className="btn-primary">
        {status === 'confirmed' ? 'Continue Analysis' : 'Continue with research analysis'}
      </button>
    </div>
  )
}
