import React from 'react'
import FileUpload from '../components/FileUpload'

export default function HomePage() {
  return (
    <div className="py-12">
      <div className="text-center mb-12">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">
          Upload Medical Report
        </h2>
        <p className="text-gray-600 max-w-2xl mx-auto">
          Upload a medical report to identify potential drug-repurposing candidates
          using neuro-symbolic AI analysis. The system will extract clinical information,
          connect to biomedical knowledge, and generate explainable candidate rankings.
        </p>
      </div>

      <FileUpload />

      <div className="mt-12 max-w-xl mx-auto">
        <h3 className="text-sm font-semibold text-gray-500 mb-3" style={{ textTransform: 'uppercase' }}>
          How it works
        </h3>
        <div className="space-y-3">
          {[
            'Upload a medical report (PDF, image, or text)',
            'AI extracts diagnoses, symptoms, and clinical entities',
            'Disease is mapped to biomedical knowledge graph',
            'Neural + symbolic reasoning identifies candidate drugs',
            'Results are ranked and explained with evidence paths',
          ].map((step, i) => (
            <div key={i} className="flex gap-3" style={{ alignItems: 'flex-start' }}>
              <span className="step-number">{i + 1}</span>
              <p className="text-sm text-gray-700">{step}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
