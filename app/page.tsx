'use client'

import { useState, useEffect } from 'react'
import Header from './components/Header'
import { translations, type Language } from './translations'

export default function Home() {
  const [language, setLanguage] = useState<Language>('zh-TW')

  // 從 localStorage 讀取語言設定
  useEffect(() => {
    const savedLang = localStorage.getItem('language') as Language
    if (savedLang && (savedLang === 'zh-TW' || savedLang === 'zh-CN' || savedLang === 'en')) {
      setLanguage(savedLang)
      document.documentElement.lang = savedLang
    } else {
      document.documentElement.lang = 'zh-TW'
    }
  }, [])

  // 儲存語言設定到 localStorage
  const handleLanguageChange = (lang: Language) => {
    setLanguage(lang)
    localStorage.setItem('language', lang)
    // 更新 HTML lang 屬性
    document.documentElement.lang = lang
  }

  const t = translations[language]

  return (
    <main>
      {/* Header with Navigation */}
      <Header currentLang={language} onLanguageChange={handleLanguageChange} />
      
      {/* Hero Section */}
      <section id="home" className="hero">
        <div className="container">
          <div className="hero-content">
            <h1>{t.heroTitle}</h1>
            <p>{t.heroDescription}</p>
            <div className="hero-buttons">
              <a href="#about" className="btn">{t.learnMore}</a>
              <a href="https://github.com/MarkChen0719/114-1Artificial-Intelligence-Methods-and-Tools" className="btn btn-secondary" target="_blank" rel="noopener noreferrer">
                <svg className="github-icon" width="16" height="16" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
                  <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path>
                </svg>
                {t.viewSource}
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="about">
        <div className="container">
          <h2>{t.about}</h2>
          <div className="about-content">
            <p>{t.aboutDescription}</p>
          </div>
        </div>
      </section>

      {/* Author Section */}
      <section className="education">
        <div className="container">
          <h2>{t.contributor}</h2>
          <div className="education-content">
            <div className="education-item">
              <p>{t.contributorName}</p>
              <p>{t.contributorEducation}</p>
            </div>
          </div>
        </div>
      </section>

      {/* Git Clone Tutorial Section */}
      <section id="git-clone" className="tutorial-section">
        <div className="container">
          <h2>{t.sectionGitClone}</h2>
          <div className="tutorial-content">
            <p>內容待補充...</p>
          </div>
        </div>
      </section>

      {/* Python Installation Section */}
      <section id="install-python" className="tutorial-section">
        <div className="container">
          <h2>{t.sectionInstallPython}</h2>
          <div className="tutorial-content">
            <p>內容待補充...</p>
          </div>
        </div>
      </section>

      {/* Virtual Environment Section */}
      <section id="venv" className="tutorial-section">
        <div className="container">
          <h2>{t.sectionVenv}</h2>
          <div className="tutorial-content">
            <p>內容待補充...</p>
          </div>
        </div>
      </section>

      {/* Requirements Installation Section */}
      <section id="requirements" className="tutorial-section">
        <div className="container">
          <h2>{t.sectionRequirements}</h2>
          <div className="tutorial-content">
            <p>內容待補充...</p>
          </div>
        </div>
      </section>

      {/* How to Run Game Section */}
      <section id="run-game" className="tutorial-section">
        <div className="container">
          <h2>{t.sectionRunGame}</h2>
          <div className="tutorial-content">
            <p>內容待補充...</p>
          </div>
        </div>
      </section>

      {/* Technical Skills Section */}
      <section className="skills">
        <div className="container">
          <h2>{t.technicalSkills}</h2>
          <div className="skills-grid">
            <div className="skill-category">
              <h3>{t.frontend}</h3>
              <div className="skill-tags">
                <span className="skill-tag">Next.js</span>
                <span className="skill-tag">React</span>
                <span className="skill-tag">TypeScript</span>
                <span className="skill-tag">JavaScript</span>
                <span className="skill-tag">HTML5</span>
                <span className="skill-tag">CSS3</span>
              </div>
            </div>
            <div className="skill-category">
              <h3>{t.backend}</h3>
              <div className="skill-tags">
                <span className="skill-tag">Python</span>
                <span className="skill-tag">MLGame</span>
                <span className="skill-tag">Pygame</span>
              </div>
            </div>
            <div className="skill-category">
              <h3>{t.aiRelated}</h3>
              <div className="skill-tags">
                <span className="skill-tag">KNN</span>
                <span className="skill-tag">Machine Learning</span>
                <span className="skill-tag">Data Collection</span>
                <span className="skill-tag">scikit-learn</span>
              </div>
            </div>
            <div className="skill-category">
              <h3>{t.tools}</h3>
              <div className="skill-tags">
                <span className="skill-tag">Git</span>
                <span className="skill-tag">GitHub</span>
                <span className="skill-tag">GitHub Pages</span>
                <span className="skill-tag">GitHub Actions</span>
                <span className="skill-tag">Docker</span>
                <span className="skill-tag">Jenkins</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="contact">
        <div className="container">
          <h2>{t.contact}</h2>
          <div className="contact-content">
            <div className="contact-card">
              <h3>{t.contactInformation}</h3>
              <div className="contact-info">
                <p>{t.email}: <a href="mailto:113207207@nccu.edu.tw">113207207@nccu.edu.tw</a></p>
                <p>{t.homepage}: <a href="https://markchen0719.github.io/my-website/" target="_blank" rel="noopener noreferrer">https://markchen0719.github.io/my-website/</a></p>
                <p>{t.location}: {t.locationValue}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="container">
          <p>{t.footer}</p>
        </div>
      </footer>
    </main>
  )
}

