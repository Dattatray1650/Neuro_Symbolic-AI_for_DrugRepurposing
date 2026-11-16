import React from 'react'

export default function ReportSummary({ summary }) {
  if (!summary) return null

  return (
    <div className="card">
      <div className="flex items-center gap-2 mb-4">
        <span>📋</span>
        <h3 className="text-lg font-semibold">Report Summary</h3>
      </div>

      <div className="space-y-4">
        {summary.condition && (
          <div>
            <h4 className="text-sm font-medium text-gray-500">Condition</h4>
            <p className="text-gray-900 font-medium">{summary.condition}</p>
            {summary.condition_status !== 'confirmed' && (
              <span className="badge" style={{ background: '#fef9c3', color: '#854d0e' }}>
                {summary.condition_status}
              </span>
            )}
          </div>
        )}

        {summary.symptoms?.length > 0 && (
          <div>
            <h4 className="text-sm font-medium text-gray-500">Symptoms</h4>
            <ul className="list-disc list-inside text-sm text-gray-700">
              {summary.symptoms.map((s, i) => <li key={i}>{s}</li>)}
            </ul>
          </div>
        )}

        {summary.clinical_findings?.length > 0 && (
          <div>
            <h4 className="text-sm font-medium text-gray-500">Clinical Findings</h4>
            <ul className="list-disc list-inside text-sm text-gray-700">
              {summary.clinical_findings.map((f, i) => <li key={i}>{f}</li>)}
            </ul>
          </div>
        )}

        {summary.biomarkers?.length > 0 && (
          <div>
            <h4 className="text-sm font-medium text-gray-500">Biomarkers</h4>
            <ul className="list-disc list-inside text-sm text-gray-700">
              {summary.biomarkers.map((b, i) => <li key={i}>{b}</li>)}
            </ul>
          </div>
        )}

        {summary.current_medications?.length > 0 && (
          <div>
            <h4 className="text-sm font-medium text-gray-500">Current Medications</h4>
            <ul className="list-disc list-inside text-sm text-gray-700">
              {summary.current_medications.map((m, i) => <li key={i}>{m}</li>)}
            </ul>
          </div>
        )}
      </div>
    </div>
  )
}
