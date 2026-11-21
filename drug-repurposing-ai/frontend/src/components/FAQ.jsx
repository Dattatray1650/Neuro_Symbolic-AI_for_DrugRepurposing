import React, { useState } from 'react'
import { ChevronDown } from 'lucide-react'

const questions = [
  {
    q: 'What is drug repurposing?',
    a: 'Drug repurposing investigates new therapeutic applications for existing drugs.'
  },
  {
    q: 'What is Neuro-Symbolic AI?',
    a: 'Neuro-Symbolic AI combines neural learning approaches with symbolic reasoning and structured knowledge.'
  },
  {
    q: 'How does this platform work?',
    a: 'The research prototype processes supported medical documents, extracts biomedical information and uses its configured reasoning pipeline to identify potential drug candidates.'
  },
  {
    q: 'Are the results clinically validated?',
    a: 'No. This is a computational research prototype. Its outputs are exploratory and require independent scientific and clinical validation.'
  },
  {
    q: 'What documents can I upload?',
    a: 'The supported document formats depend on the current backend upload implementation.'
  }
]

export default function FAQ() {
  const [active, setActive] = useState(null)

  return (
    <section className="section faq-section" id="faq">

      <div className="section-heading">
        <span className="eyebrow">FAQ</span>
        <h2>Frequently Asked <span>Questions</span></h2>
      </div>

      <div className="faq-list">

        {questions.map((item, index) => (
          <div className="faq-item" key={index}>

            <button
              className="faq-question"
              onClick={() => setActive(active === index ? null : index)}
              aria-expanded={active === index}
            >
              {item.q}
              <ChevronDown className={active === index ? 'rotated' : ''} />
            </button>

            {active === index && (
              <div className="faq-answer">
                {item.a}
              </div>
            )}

          </div>
        ))}

      </div>

    </section>
  )
}