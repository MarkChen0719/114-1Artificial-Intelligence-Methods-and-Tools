'use client'

import { useState, useEffect } from 'react'
import Button from './Button'
import LanguageSwitcher from './LanguageSwitcher'
import { translations, type Language } from '../translations'

interface HeaderProps {
  currentLang: Language
  onLanguageChange: (lang: Language) => void
}

export default function Header({ currentLang, onLanguageChange }: HeaderProps) {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const t = translations[currentLang]

  const scrollToSection = (id: string) => {
    const element = document.getElementById(id)
    if (element) {
      const headerOffset = 80
      const elementPosition = element.getBoundingClientRect().top
      const offsetPosition = elementPosition + window.pageYOffset - headerOffset

      window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
      })
    }
    setIsMenuOpen(false)
  }

  const navItems = [
    { id: 'home', label: t.navHome || '首頁' },
    { id: 'git-clone', label: t.navGitClone || 'Git Clone 教學' },
    { id: 'install-python', label: t.navInstallPython || 'Python 安裝教學' },
    { id: 'venv', label: t.navVenv || '建立虛擬環境' },
    { id: 'requirements', label: t.navRequirements || '安裝 requirements.txt' },
    { id: 'run-game', label: t.navRunGame || '遊戲如何執行' },
    { id: 'contact', label: t.navContact || '聯絡資訊' },
  ]

  return (
    <header className="navbar">
      <div className="container">
        <div className="navbar-content">
          <div className="navbar-logo">
            <button
              onClick={() => scrollToSection('home')}
              className="navbar-logo-button"
            >
              <h1>魷魚遊戲</h1>
            </button>
          </div>
          
          {/* Desktop Navigation */}
          <nav className="navbar-nav">
            {navItems.map((item) => (
              <Button
                key={item.id}
                variant="ghost"
                size="sm"
                onClick={() => scrollToSection(item.id)}
                className="navbar-button"
              >
                {item.label}
              </Button>
            ))}
          </nav>

          <div className="navbar-actions">
            <LanguageSwitcher currentLang={currentLang} onLanguageChange={onLanguageChange} />
            
            {/* Mobile Menu Button */}
            <button
              className="navbar-menu-button"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              aria-label="Toggle menu"
            >
              <svg
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                {isMenuOpen ? (
                  <>
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                  </>
                ) : (
                  <>
                    <line x1="3" y1="12" x2="21" y2="12"></line>
                    <line x1="3" y1="6" x2="21" y2="6"></line>
                    <line x1="3" y1="18" x2="21" y2="18"></line>
                  </>
                )}
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <nav className="navbar-mobile">
            {navItems.map((item) => (
              <Button
                key={item.id}
                variant="ghost"
                size="default"
                onClick={() => scrollToSection(item.id)}
                className="navbar-mobile-button"
              >
                {item.label}
              </Button>
            ))}
          </nav>
        )}
      </div>
    </header>
  )
}

