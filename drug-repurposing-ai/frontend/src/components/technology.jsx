import React from 'react'
import {
  BrainCircuit,
  Network,
  Microscope,
  Database,
  GitBranch
} from 'lucide-react'

const technologies = [
  {
    icon: BrainCircuit,
    title: 'Neural Intelligence',
    description: 'AI-driven analysis to identify meaningful biomedical patterns.'
  },
  {
    icon: Network,
    title: 'Knowledge Graphs',
    description: 'Connect diseases, genes, proteins and potential drug candidates.'
  },
  {
    icon: Microscope,
    title: 'Biomedical NLP',
    description: 'Extract relevant biomedical information from supported documents.'
  },
  {
    icon: Database,
    title: 'Biomedical Databases',
    description: 'Use structured biomedical knowledge as a research foundation.'
  },
  {
    icon: GitBranch,
    title: 'Symbolic Reasoning',
    description: 'Represent relationships and provide interpretable reasoning paths.'
  }
]

export default function Technology() {
  return (
    <section className="technology-section" id="technology">
      <div className="section-heading">
        <span className="eyebrow">OUR TECHNOLOGY</span>
        <h2>Built on <span>Intelligent Science</span></h2>
        <p>Combining computational intelligence with structured biomedical knowledge.</p>
      </div>

      <div className="technology-grid">
        {technologies.map((item, index) => {
          const Icon = item.icon

          return (
            <div className="technology-card" key={index}>
              <Icon size={30} />
              <h3>{item.title}</h3>
              <p>{item.description}</p>
            </div>
          )
        })}
      </div>
    </section>
  )
}