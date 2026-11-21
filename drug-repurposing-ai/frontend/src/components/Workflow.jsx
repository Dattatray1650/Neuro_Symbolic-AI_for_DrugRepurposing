import React from 'react'
import {
  Upload,
  FileSearch,
  BrainCircuit,
  Network,
  Pill,
  FileCheck
} from 'lucide-react'

const steps = [
  {
    icon: Upload,
    title: 'Document Upload',
    description: 'Upload a supported medical document.'
  },
  {
    icon: FileSearch,
    title: 'Information Extraction',
    description: 'Extract relevant biomedical information.'
  },
  {
    icon: BrainCircuit,
    title: 'Neural Analysis',
    description: 'Identify meaningful patterns using AI.'
  },
  {
    icon: Network,
    title: 'Knowledge Mapping',
    description: 'Connect biomedical entities and relationships.'
  },
  {
    icon: Pill,
    title: 'Candidate Identification',
    description: 'Explore potential drug-repurposing candidates.'
  },
  {
    icon: FileCheck,
    title: 'Results & Explanation',
    description: 'Review research findings and their explanations.'
  }
]

export default function Workflow() {
  return (
    <section className="workflow-section" id="workflow">
      <div className="section-heading">
        <span className="eyebrow">HOW IT WORKS</span>
        <h2>From Medical Data to <span>Research Insights</span></h2>
        <p>A structured computational workflow for exploratory drug-repurposing research.</p>
      </div>

      <div className="workflow-grid">
        {steps.map((step, index) => {
          const Icon = step.icon

          return (
            <div className="workflow-card" key={index}>
              <span className="workflow-number">0{index + 1}</span>
              <Icon size={30} />
              <h3>{step.title}</h3>
              <p>{step.description}</p>
            </div>
          )
        })}
      </div>
    </section>
  )
}