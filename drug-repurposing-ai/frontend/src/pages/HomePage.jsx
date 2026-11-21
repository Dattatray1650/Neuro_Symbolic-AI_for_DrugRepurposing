import React from 'react'

import Navbar from '../components/Navbar'
import Hero from '../components/Hero'
import Features from '../components/Features'
import About from '../components/About'
import Workflow from '../components/Workflow'
import Technology from '../components/Technology'
import Feedback from '../components/Feedback'
import FAQ from '../components/FAQ'
import Footer from '../components/Footer'

import FileUpload from '../components/FileUpload'
import Disclaimer from '../components/Disclaimer'

export default function HomePage() {
  return (
    <>
      <Navbar />

      <main>
        <Hero />
        <Features />
        <About />
        <Workflow />
        <Technology />

        <section className="workspace-section" id="workspace">
          <div className="section-heading">
            <span className="eyebrow">AI RESEARCH WORKSPACE</span>
            <h2>
              Start Your <span>Drug Repurposing Analysis</span>
            </h2>
            <p>
              Upload your supported medical document
              to begin the computational research workflow.
            </p>
          </div>

          <div className="upload-container">
            <Disclaimer />
            <FileUpload />
          </div>
        </section>

        <Feedback />
        <FAQ />
      </main>

      <Footer />
    </>
  )
}