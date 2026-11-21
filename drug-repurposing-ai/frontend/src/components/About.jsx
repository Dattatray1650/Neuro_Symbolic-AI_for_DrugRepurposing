import React from 'react'
import { Dna, Brain, Network } from 'lucide-react'

export default function About() {
  return (
    <section className="section about-section" id="about">

      <div className="about-visual">
        <div className="about-visual-inner">
          <Dna size={100} strokeWidth={1} />

          <div className="orbit orbit-one"></div>
          <div className="orbit orbit-two"></div>

          <div className="about-label">
            NEURO-SYMBOLIC INTELLIGENCE
          </div>
        </div>
      </div>

      <div className="about-content">

        <span className="eyebrow">ABOUT THE PROJECT</span>

        <h2>
          Connecting Two Worlds of
          <span> Artificial Intelligence</span>
        </h2>

        <p>
          Drug repurposing explores new therapeutic applications
          for existing drugs. Our research prototype investigates
          how neuro-symbolic AI can support this process using
          biomedical information and structured knowledge.
        </p>

        <div className="about-point">
          <Brain size={23} />
          <div>
            <h4>Neural Processing</h4>
            <p>Extracting meaningful biomedical information.</p>
          </div>
        </div>

        <div className="about-point">
          <Network size={23} />
          <div>
            <h4>Symbolic Reasoning</h4>
            <p>Connecting extracted information with biomedical knowledge.</p>
          </div>
        </div>

      </div>

    </section>
  )
}