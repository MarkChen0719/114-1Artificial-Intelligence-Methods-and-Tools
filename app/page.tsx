export default function Home() {
  return (
    <main>
      {/* Hero Section */}
      <section className="hero">
        <div className="container">
          <div className="hero-content">
            <h1>魷魚遊戲!</h1>
            <p>
              這是一個基於機器學習與 SDGs14 製作的破關小遊戲，我們希望同學們與小朋友們能夠真正地從機器學習的角度認識 AI，與此同時，去認識到海洋垃圾對於環境的危害。
            </p>
            <div className="hero-buttons">
              <a href="#about" className="btn">了解更多</a>
              <a href="https://github.com/MarkChen0719/114-1Artificial-Intelligence-Methods-and-Tools" className="btn btn-secondary" target="_blank" rel="noopener noreferrer">
                <svg className="github-icon" width="16" height="16" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
                  <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path>
                </svg>
                查看原始碼
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="about">
        <div className="container">
          <h2>About</h2>
          <div className="about-content">
            <p>
              這是一個基於機器學習與 SDGs14 製作的破關小遊戲，我們希望同學們與小朋友們能夠真正地從機器學習的角度認識 AI，與此同時，去認識到海洋垃圾對於環境的危害。
            </p>
          </div>
        </div>
      </section>

      {/* Author Section */}
      <section className="education">
        <div className="container">
          <h2>作者</h2>
          <div className="education-content">
            <div className="education-item">
              <p>Contributor: Wei-Jun Chen, National Chengchi University, B.B.S. in Statistics</p>
            </div>
          </div>
        </div>
      </section>

      {/* Technical Skills Section */}
      <section className="skills">
        <div className="container">
          <h2>Technical Skills</h2>
          <div className="skills-grid">
            <div className="skill-category">
              <h3>Frontend</h3>
              <div className="skill-tags">
                <span className="skill-tag">Next.js</span>
                <span className="skill-tag">React</span>
                <span className="skill-tag">TypeScript</span>
                <span className="skill-tag">JavaScript</span>
                <span className="skill-tag">HTML5</span>
                <span className="skill-tag">CSS3</span>
                <span className="skill-tag">shadcn/ui</span>
              </div>
            </div>
            <div className="skill-category">
              <h3>Backend</h3>
              <div className="skill-tags">
                <span className="skill-tag">Python</span>
                <span className="skill-tag">MLGame</span>
              </div>
            </div>
            <div className="skill-category">
              <h3>AI_Related</h3>
              <div className="skill-tags">
                <span className="skill-tag">KNN</span>
                <span className="skill-tag">Machine Learning</span>
                <span className="skill-tag">Data Collection</span>
              </div>
            </div>
            <div className="skill-category">
              <h3>Tools</h3>
              <div className="skill-tags">
                <span className="skill-tag">Git</span>
                <span className="skill-tag">GitHub</span>
                <span className="skill-tag">GitHub Pages</span>
                <span className="skill-tag">GitHub Actions</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="contact">
        <div className="container">
          <h2>Contact</h2>
          <div className="contact-content">
            <div className="contact-card">
              <h3>Contact Information</h3>
              <div className="contact-info">
                <p>Email: <a href="mailto:113207207@nccu.edu.tw">113207207@nccu.edu.tw</a></p>
                <p>homepage: <a href="https://markchen0719.github.io/my-website/" target="_blank" rel="noopener noreferrer">https://markchen0719.github.io/my-website/</a></p>
                <p>Location: Taipei, Taiwan</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="container">
          <p>© 2025 Wei-Jun Chen · Built with Next.js & shadcn/ui</p>
        </div>
      </footer>
    </main>
  )
}

