import React from 'react'
import {
  BrainCircuit,
  Network,
  FlaskConical,
  ShieldCheck
} from 'lucide-react'

const features = [
  {
    icon: BrainCircuit,
    title: 'Neural Intelligence',
    description: 'Extract biomedical entities and discover meaningful patterns from medical documents.'
  },
  {
    icon: Network,
    title: 'Knowledge Graphs',
    description: 'Explore relationships between diseases, genes, proteins and potential drug candidates.'
  },
  {
    icon: FlaskConical,
    title: 'Drug Repurposing',
    description: 'Investigate existing drugs for potential alternative therapeutic applications.'
  },
  {
    icon: ShieldCheck,
    title: 'Explainable AI',
    description: 'Understand the reasoning and evidence behind computational drug recommendations.'
  }
]

export default function Features() {
  return (
    <section className="section features-section" id="features">

      <div className="section-heading">
        <span className="eyebrow">OUR CAPABILITIES</span>
        <h2>Intelligence Meets <span>Biological Reasoning</span></h2>
        <p>
          Combining computational intelligence with structured
          biomedical knowledge.
        </p>
      </div>

      <div className="features-grid">
        {features.map((item, index) => {
          const Icon = item.icon

          return (
            <div className="feature-card" key={index}>
              <div className="feature-icon">
                <Icon size={27} />
              </div>

              <h3>{item.title}</h3>
              <p>{item.description}</p>

              <span className="feature-number">
                0{index + 1}
              </span>
            </div>
          )
        })}
      </div>

    </section>
  )
}