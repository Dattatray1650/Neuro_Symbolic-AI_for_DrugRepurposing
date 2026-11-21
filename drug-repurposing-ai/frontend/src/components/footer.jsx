import React from 'react'
import { Dna, ArrowUp } from 'lucide-react'

export default function Footer() {
  return (
    <footer className="site-footer" id="contact">

      <div className="footer-content">

        <div className="footer-brand">
          <Dna size={30} />
          <h3>NeuroRepurpose</h3>

          <p>
            Exploring drug repurposing through
            neuro-symbolic artificial intelligence.
          </p>
        </div>

        <div className="footer-links">
          <h4>Explore</h4>
          <a href="#home">Home</a>
          <a href="#about">About</a>
          <a href="#technology">Technology</a>
          <a href="#workflow">How It Works</a>
        </div>

        <div className="footer-links">
          <h4>Research</h4>
          <a href="#workspace">AI Workspace</a>
          <a href="#features">Capabilities</a>
          <a href="#faq">FAQ</a>
        </div>

      </div>

      <div className="footer-bottom">
        <p>© {new Date().getFullYear()} NeuroRepurpose. Research Prototype.</p>

        <a href="#home" aria-label="Back to top">
          Back to top <ArrowUp size={15} />
        </a>
      </div>

      <p className="footer-disclaimer">
        For research and educational purposes only. Not intended for clinical diagnosis or treatment decisions.
      </p>

    </footer>
  )
}
