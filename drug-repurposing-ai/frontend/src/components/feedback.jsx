import React from 'react'
import { MessageSquare, ArrowRight } from 'lucide-react'

export default function Feedback() {
  return (
    <section className="section feedback-section" id="feedback">

      <div className="feedback-content">
        <span className="eyebrow">RESEARCH COMMUNITY</span>

        <h2>
          Your Insights Can Help
          <span> Improve Our Research</span>
        </h2>

        <p>
          We welcome feedback from students, researchers and
          technology enthusiasts exploring AI-driven drug repurposing.
        </p>

        <a href="mailto:feedback@example.com" className="primary-btn">
          Share Your Feedback <ArrowRight size={18} />
        </a>
      </div>

      <div className="feedback-icon">
        <MessageSquare size={85} strokeWidth={1} />
      </div>

    </section>
  )
}