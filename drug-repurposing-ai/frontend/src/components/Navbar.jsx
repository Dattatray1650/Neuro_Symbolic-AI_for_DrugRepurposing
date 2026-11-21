import React, { useState } from 'react'
import { Menu, X, Dna } from 'lucide-react'

export default function Navbar() {
  const [open, setOpen] = useState(false)

  const links = [
    ['Home', '#home'],
    ['About', '#about'],
    ['Technology', '#technology'],
    ['How It Works', '#workflow'],
    ['Contact', '#contact']
  ]

  return (
    <nav className="navbar">
      <a href="#home" className="brand">
        <span className="brand-icon"><Dna size={27} /></span>
        <span>
          <strong>NeuroRepurpose</strong>
          <small>AI Research Platform</small>
        </span>
      </a>

      <div className={`nav-links ${open ? 'active' : ''}`}>
        {links.map(([name, link]) => (
          <a key={name} href={link} onClick={() => setOpen(false)}>
            {name}
          </a>
        ))}

        <a href="#workspace" className="nav-button" onClick={() => setOpen(false)}>
          Start Analysis →
        </a>
      </div>

      <button className="mobile-menu" onClick={() => setOpen(!open)}
        aria-label="Toggle navigation">
        {open ? <X /> : <Menu />}
      </button>
    </nav>
  )
}