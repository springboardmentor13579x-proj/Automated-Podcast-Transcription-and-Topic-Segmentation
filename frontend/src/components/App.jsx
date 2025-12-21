import React, { useState, useEffect } from 'react';
import './styles/main.css';

import Home from './components/Home';
import Transcription from './components/Transcription';
import Quality from './components/Quality';
import Segments from './components/Segments';
import TopicSearch from './components/TopicSearch';
import Downloads from './components/Downloads';

function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const [processedData, setProcessedData] = useState(null);
  const [currentFile, setCurrentFile] = useState(null);

  // SAFE particle initialization (FIXED)
  useEffect(() => {
    setTimeout(() => {
      createParticles();
    }, 100);
  }, []);

  const createParticles = () => {
    const particlesContainer = document.getElementById('particles');
    if (!particlesContainer) return;

    particlesContainer.innerHTML = ""; // prevent duplicates

    for (let i = 0; i < 30; i++) {
      const particle = document.createElement('div');
      particle.className = 'particle';
      particle.style.left = Math.random() * 100 + '%';
      particle.style.top = Math.random() * 100 + '%';
      particle.style.animationDelay = Math.random() * 10 + 's';
      particle.style.animationDuration = (15 + Math.random() * 10) + 's';
      particlesContainer.appendChild(particle);
    }
  };

  const showNotification = (message, type = 'success') => {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.style.cssText = `
      position: fixed;
      bottom: 20px;
      right: 20px;
      background: ${
        type === 'error'
          ? 'linear-gradient(135deg, #ff4444, #cc0000)'
          : 'linear-gradient(135deg, var(--primary), var(--secondary))'
      };
      color: white;
      padding: 15px 25px;
      border-radius: 10px;
      box-shadow: 0 10px 30px rgba(0, 212, 255, 0.4);
      z-index: 10000;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
      notification.remove();
    }, 3000);
  };

  return (
    <div className="app">

      {/* DNA Helix Background */}
      <div className="dna-helix">
        <div className="dna-strand"></div>
        <div className="dna-strand"></div>
        <div className="dna-strand"></div>
      </div>

      {/* Floating Particles */}
      <div className="particles" id="particles"></div>

      {/* Navigation */}
      <nav>
        <div className="nav-container">
          <div className="logo">
            <i className="fas fa-stethoscope"></i>
            <span>MedicalPodcastAI</span>
          </div>

          <ul className="nav-links">
            <li>
              <a href="#" onClick={(e) => { e.preventDefault(); setCurrentPage('home'); }}
                 className={currentPage === 'home' ? 'nav-link active' : 'nav-link'}>
                Home
              </a>
            </li>

            <li>
              <a href="#" onClick={(e) => { e.preventDefault(); setCurrentPage('transcription'); }}
                 className={currentPage === 'transcription' ? 'nav-link active' : 'nav-link'}>
                Transcription
              </a>
            </li>

            <li>
              <a href="#" onClick={(e) => { e.preventDefault(); setCurrentPage('quality'); }}
                 className={currentPage === 'quality' ? 'nav-link active' : 'nav-link'}>
                Quality
              </a>
            </li>

            <li>
              <a href="#" onClick={(e) => { e.preventDefault(); setCurrentPage('segments'); }}
                 className={currentPage === 'segments' ? 'nav-link active' : 'nav-link'}>
                Segments
              </a>
            </li>

            <li>
              <a href="#" onClick={(e) => { e.preventDefault(); setCurrentPage('topic-search'); }}
                 className={currentPage === 'topic-search' ? 'nav-link active' : 'nav-link'}>
                Topic Search
              </a>
            </li>

            <li>
              <a href="#" onClick={(e) => { e.preventDefault(); setCurrentPage('downloads'); }}
                 className={currentPage === 'downloads' ? 'nav-link active' : 'nav-link'}>
                Downloads
              </a>
            </li>
          </ul>
        </div>
      </nav>

      {/* Pages */}
      {currentPage === 'home' && (
        <Home
          setProcessedData={setProcessedData}
          setCurrentFile={setCurrentFile}
          setCurrentPage={setCurrentPage}
          showNotification={showNotification}
        />
      )}

      {currentPage === 'transcription' && (
        <Transcription
          processedData={processedData}
          currentFile={currentFile}
        />
      )}

      {currentPage === 'quality' && (
        <Quality
          showNotification={showNotification}
        />
      )}

      {currentPage === 'segments' && (
        <Segments processedData={processedData} />
      )}

      {currentPage === 'topic-search' && (
        <TopicSearch
          processedData={processedData}
          showNotification={showNotification}
        />
      )}

      {currentPage === 'downloads' && (
        <Downloads
          processedData={processedData}
          showNotification={showNotification}
        />
      )}
    </div>
  );
}

export default App;
