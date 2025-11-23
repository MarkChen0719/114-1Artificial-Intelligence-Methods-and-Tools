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

  const handleNavClick = (id: string) => {
    setIsMenuOpen(false)
    // 使用錨點連結，讓瀏覽器自然處理滾動
    window.location.hash = id
  }

  const navItems = [
    { id: 'home', label: t.navHome || '首頁' },
    { id: 'environment', label: t.navEnvironment || '環境安裝' },
    { id: 'manual', label: t.navManual || '手動操控' },
    { id: 'collect', label: t.navCollect || '收集資料' },
    { id: 'train', label: t.navTrain || '訓練模型' },
    { id: 'knn', label: t.navKNN || '使用模型' },
    { id: 'template', label: t.navTemplate || '自定義模板' },
    { id: 'speed', label: t.navSpeed || '加速遊戲' },
    { id: 'contact', label: t.navContact || '聯絡資訊' },
  ]

  return (
    <header className="navbar">
      <div className="container">
        <div className="navbar-content">
          <div className="navbar-logo">
            <a
              href="#home"
              className="navbar-logo-button"
            >
              <h1>魷魚遊戲</h1>
            </a>
          </div>
          
          {/* Desktop Navigation */}
          <nav className="navbar-nav">
            {navItems.map((item) => (
              <a
                key={item.id}
                href={`#${item.id}`}
                className="navbar-button"
                onClick={() => handleNavClick(item.id)}
              >
                {item.label}
              </a>
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
              <a
                key={item.id}
                href={`#${item.id}`}
                className="navbar-mobile-button"
                onClick={() => handleNavClick(item.id)}
              >
                {item.label}
              </a>
            ))}
          </nav>
        )}
      </div>
    </header>
  )
}

