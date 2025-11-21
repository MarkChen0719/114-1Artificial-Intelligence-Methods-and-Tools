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
              <a href="https://github.com/MarkChen0719/114-1Artificial-Intelligence-Methods-and-Tools" className="btn btn-secondary" target="_blank" rel="noopener noreferrer">查看原始碼</a>
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

      {/* Education Section */}
      <section className="education">
        <div className="container">
          <h2>Education</h2>
          <div className="education-content">
            <div className="education-item">
              <p>作者：陳維竣</p>
              <p>國立政治大學</p>
              <p>（目前暫定，之後會新增內容）</p>
            </div>
          </div>
        </div>
      </section>

      {/* Technical Skills Section */}
      <section className="skills">
        <div className="container">
          <h2>用到的技術</h2>
          <div className="skills-content">
            <p>用到的技術：</p>
            <p>前端：Next.js & shadcn/ui</p>
            <p>後端：Python</p>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="contact">
        <div className="container">
          <h2>Contact</h2>
          <div className="contact-content">
            <h3>Contact Information</h3>
            <div className="contact-info">
              <p>Email: 113207207@nccu.edu.tw</p>
              <p>Location: Taipei, Taiwan</p>
            </div>
          </div>
        </div>
      </section>
    </main>
  )
}

