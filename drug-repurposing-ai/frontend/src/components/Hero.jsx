import React from 'react'
import { ArrowRight, Microscope, Sparkles } from 'lucide-react'

export default function Hero() {
  return (
    <section className="hero-section" id="home">

      <div className="hero-content">

        <div className="hero-tag">
          <Sparkles size={15} />
          NEXT-GENERATION BIOMEDICAL AI
        </div>

        <h1>
          Rethinking Drug Discovery Through
          <span> Neuro-Symbolic AI.</span>
        </h1>

        <p>
          Bridging artificial intelligence and symbolic reasoning
          to explore potential drug repurposing opportunities
          through explainable biomedical intelligence.
        </p>

        <div className="hero-buttons">
          <a href="#workspace" className="primary-btn">
            Explore AI Platform <ArrowRight size={18} />
          </a>

          <a href="#about" className="secondary-btn">
            Discover Our Research
          </a>
        </div>

        <div className="hero-trust">
          <Microscope size={19} />
          <span>Research-focused • Explainable • Knowledge-driven</span>
        </div>

      </div>

      <div className="hero-image-wrapper">
        <img
          src="/src/assets/hero.png"
          alt="Scientific molecular visualization"
          className="hero-image"
        />

        <div className="floating-card floating-card-one">
          <span className="floating-dot"></span>
          Neural Intelligence
        </div>

        <div className="floating-card floating-card-two">
          <span className="floating-dot"></span>
          Symbolic Reasoning
        </div>
      </div>

    </section>
  )
}