import React, { useState, useEffect, useRef } from "react";
import "./App.css";

// Import Chart.js components
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import { Bar, Line, Doughnut } from 'react-chartjs-2';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

const API = process.env.REACT_APP_API || "http://127.0.0.1:5000";

export default function App() {
  // State management
  const [page, setPage] = useState("home");
  const [processedData, setProcessedData] = useState(null);
  const [currentFile, setCurrentFile] = useState(null);
  const [progress, setProgress] = useState(0);
  const [uploading, setUploading] = useState(false);
  const [quality, setQuality] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [searchMessage, setSearchMessage] = useState("");
  const [notification, setNotification] = useState({ show: false, message: "", type: "" });

  // Refs
  const particlesRef = useRef(null);
  const progressRef = useRef(null);
  const fileInputRef = useRef(null);

  // --- Load data from localStorage on initial render ---
  useEffect(() => {
    const savedData = localStorage.getItem('processedData');
    if (savedData) {
      const parsedData = JSON.parse(savedData);
      setProcessedData(parsedData);
      if (parsedData.avg_accuracy) {
        setQuality(parsedData);
      }
    }
    const savedFile = localStorage.getItem('currentFile');
    if (savedFile) {
      setCurrentFile(JSON.parse(savedFile));
    }
  }, []);

  // --- Save data to localStorage whenever it changes ---
  useEffect(() => {
    if (processedData) {
      localStorage.setItem('processedData', JSON.stringify(processedData));
    }
  }, [processedData]);

  useEffect(() => {
    if (currentFile) {
      localStorage.setItem('currentFile', JSON.stringify({
        name: currentFile.name,
        size: currentFile.size,
        type: currentFile.type,
        lastModified: currentFile.lastModified
      }));
    }
  }, [currentFile]);

  // Initialize particles
  useEffect(() => {
    if (!particlesRef.current) return;
    const particlesContainer = particlesRef.current;
    particlesContainer.innerHTML = "";

    for (let i = 0; i < 30; i++) {
      const particle = document.createElement("div");
      particle.className = "particle";
      particle.style.left = Math.random() * 100 + "%";
      particle.style.top = Math.random() * 100 + "%";
      particle.style.animationDelay = Math.random() * 10 + "s";
      particle.style.animationDuration = (15 + Math.random() * 10) + "s";
      particlesContainer.appendChild(particle);
    }
  }, []);

  // Helper functions
  const showNotification = (message, type = "success") => {
    setNotification({ message, type, show: true });
    setTimeout(() => {
      setNotification({ show: false, message: "", type: "" });
    }, 3000);
  };

  const showPage = (pageId) => {
    setPage(pageId);
  };

  const clearResults = () => {
    if (window.confirm("Are you sure you want to clear all results and uploaded file data? This action cannot be undone.")) {
      setProcessedData(null);
      setQuality(null);
      setCurrentFile(null);
      setSearchQuery("");
      setSearchResults([]);
      setSearchMessage("");
      setProgress(0);
      
      localStorage.removeItem('processedData');
      localStorage.removeItem('currentFile');
      
      showNotification("All results have been cleared.", "success");
      showPage("home");
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  };

  // Handle file upload
  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const allowedTypes = ["audio/wav", "audio/mp3", "audio/m4a", "audio/flac", "audio/ogg"];
    if (!allowedTypes.includes(file.type) && !file.name.match(/\.(wav|mp3|m4a|flac|ogg)$/i)) {
      showNotification("Please upload a valid audio file (WAV, MP3, M4A, FLAC, OGG)", "error");
      return;
    }

    setCurrentFile(file);
    setUploading(true);
    setProgress(10);

    progressRef.current = setInterval(() => {
      setProgress((p) => (p < 90 ? p + 5 : p));
    }, 800);

    try {
      const formData = new FormData();
      formData.append("audio", file);

      console.log("Attempting to fetch from:", `${API}/upload`);
      const res = await fetch(`${API}/upload`, { method: "POST", body: formData });
      
      console.log("Fetch response received. Status:", res.status, res.statusText);
      
      if (!res.ok) {
        // Attempt to get more error details from the response body
        const errorText = await res.text();
        console.error("Server response body:", errorText);
        throw new Error(`Server error: ${res.status} ${res.statusText}. Details: ${errorText}`);
      }

      const data = await res.json();
      console.log("Successfully parsed JSON from backend:", data);

      clearInterval(progressRef.current);

      if (data.status !== "completed") {
        throw new Error(data.error || "Processing failed");
      }

      const allData = {
        transcript: data.transcript,
        segments: data.segments,
        avg_accuracy: data.avg_accuracy,
        avg_wer: data.avg_wer,
        avg_cer: data.avg_cer,
        avg_similarity: data.avg_similarity,
        fileInfo: {
          name: file.name,
          size: file.size,
          type: file.type,
          lastModified: file.lastModified,
        },
      };
      
      setProcessedData(allData);
      setQuality(allData);
      
      setProgress(100);
      showNotification("File processed successfully!", "success");
      showPage("transcription");

    } catch (e) {
      console.error("Upload failed with exception:", e);
      showNotification(e.message, "error");
    } finally {
      setUploading(false);
    }
  };

  // Topic search functionality
  const searchTopic = () => {
    if (!searchQuery.trim()) {
      setSearchMessage("Please enter a medical topic to search.");
      setSearchResults([]);
      return;
    }
    if (!processedData || !processedData.segments) {
      setSearchMessage("Please upload an audio file first.");
      setSearchResults([]);
      return;
    }

    const matches = processedData.segments.filter(seg =>
      (seg.segment_text || "").toLowerCase().includes(searchQuery.toLowerCase()) ||
      (seg.keywords || []).some(k => k.toLowerCase().includes(searchQuery.toLowerCase()))
    );

    if (matches.length === 0) {
      setSearchMessage(`No matching topic found for "${searchQuery}".`);
      setSearchResults([]);
    } else {
      setSearchMessage("");
      setSearchResults(matches);
    }
  };

  const handleSearchKeyPress = (e) => {
    if (e.key === "Enter") {
      searchTopic();
    }
  };

  const downloadFile = (type) => {
    if (!processedData && !["transcript", "quality"].includes(type)) {
      showNotification("Please upload an audio file first", "error");
      return;
    }

    showNotification(`Preparing ${type} download...`);

    let content = "";
    let filename = "";
    let mimeType = "text/plain";

    switch (type) {
      case "transcript":
        content = processedData?.transcript || "No transcript available";
        filename = "transcript.txt";
        break;
      case "segments":
        content = JSON.stringify(processedData?.segments || [], null, 2);
        filename = "segments.json";
        mimeType = "application/json";
        break;
      case "keywords":
        const allKeywords = [...new Set(processedData?.segments?.flatMap(seg => seg.keywords) || [])];
        content = allKeywords.join("\n");
        filename = "keywords.txt";
        break;
      case "quality":
        if (quality) {
          content = `Quality Report\n\nAccuracy: ${quality.avg_accuracy}%\nWord Error Rate: ${quality.avg_wer}%\nCharacter Error Rate: ${quality.avg_cer}%\nSemantic Similarity: ${quality.avg_similarity}\n\nFile: ${currentFile?.name || "Unknown"}\nSize: ${currentFile ? formatFileSize(currentFile.size) : "Unknown"}`;
          filename = "quality_report.txt";
        }
        break;
      case "summary":
        content = `Medical Audio Summary\n\n${processedData?.segments?.map(seg => `${seg.segment_label}: ${seg.segment_summary}`).join("\n\n") || "No summary available"}`;
        filename = "summary.txt";
        break;
      case "all":
        content = `Complete Package\n\nTRANSCRIPT:\n${processedData?.transcript || "No transcript available"}\n\nSEGMENTS:\n${JSON.stringify(processedData?.segments || [], null, 2)}`;
        filename = "complete_package.txt";
        break;
      default:
        return;
    }

    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    showNotification(`${type.charAt(0).toUpperCase() + type.slice(1)} downloaded successfully!`);
  };

  const highlightMedicalTerms = (text) => {
    if (!text) return "<p>No transcript available</p>";
    const medicalTerms = ['pain', 'fever', 'chest', 'breath', 'anxiety', 'insomnia', 
                         'cardiac', 'vital', 'crackles', 'COVID-19', 'ECG', 'X-ray',
                         'BP', 'blood pressure', 'heart rate', 'temperature', 'oxygen',
                         'hypertension', 'diabetes', 'medications', 'dizziness', 'fatigue'];
    
    let highlightedText = text;
    medicalTerms.forEach(term => {
        const regex = new RegExp(`\\b(${term})\\b`, 'gi');
        highlightedText = highlightedText.replace(regex, 
            '<span class="medical-term">$1</span>');
    });
    
    return `<p>${highlightedText.replace(/\n/g, '</p><p>')}</p>`;
  };

  const highlightSearchTerm = (text, term) => {
    if (!text || !term) return text;
    const regex = new RegExp(`(${term})`, 'gi');
    return text.replace(regex, '<span style="background: rgba(0, 212, 255, 0.3); padding: 2px 4px; border-radius: 4px;">$1</span>');
  };

  // --- FIX: Add checks to prevent runtime errors by providing default values ---
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: { color: 'white' }
      },
      title: {
        display: true,
        color: 'white',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        grid: { color: 'rgba(255, 255, 255, 0.1)' },
        ticks: { color: 'white' }
      },
      x: {
        grid: { color: 'rgba(255, 255, 255, 0.1)' },
        ticks: { color: 'white' }
      }
    }
  };

  const barData = {
    labels: ['Accuracy', 'WER', 'CER'],
    datasets: [
      {
        label: 'Percentage (%)',
        data: [
          quality?.avg_accuracy || 0, 
          quality?.avg_wer || 0, 
          quality?.avg_cer || 0
        ],
        backgroundColor: 'rgba(0, 212, 255, 0.5)',
        borderColor: 'rgba(0, 212, 255, 1)',
        borderWidth: 1,
      },
    ],
  };

  // FIXED: More honest WER trend data
  const lineData = {
    labels: ['Segment 1', 'Segment 2', 'Segment 3', 'Segment 4'],
    datasets: [
      {
        label: 'WER Trend (Illustrative)',
        data: processedData?.segments
          ? processedData.segments.map(() => quality?.avg_wer || 0)
          : [],
        fill: false,
        borderColor: 'rgb(240, 147, 251)',
        tension: 0.1,
      },
    ],
  };
  
  // FIXED: Convert similarity from 0-1 range to 0-100 for the chart
  const similarityPercent = (quality?.avg_similarity || 0) * 100;
  const doughnutData = {
    labels: ['Similarity', 'Dissimilarity'],
    datasets: [
      {
        label: 'Semantic Similarity',
        data: [
          similarityPercent,
          100 - similarityPercent
        ],
        backgroundColor: [
          'rgba(102, 126, 234, 0.7)',
          'rgba(255, 255, 255, 0.1)',
        ],
        borderColor: [
          'rgba(102, 126, 234, 1)',
          'rgba(255, 255, 255, 0.3)',
        ],
        borderWidth: 1,
      },
    ],
  };

  return (
    <>
      <div className="dna-helix">
        <div className="dna-strand"></div>
        <div className="dna-strand"></div>
        <div className="dna-strand"></div>
      </div>

      <div className="particles" ref={particlesRef}></div>

      <nav>
        <div className="nav-container">
          <div className="logo">
            <i className="fas fa-stethoscope"></i>
            <span>MedicalPodcastAI</span>
          </div>
          <ul className="nav-links">
            {/* --- FIX: Replaced <a> with <button> for navigation --- */}
            <li><button onClick={() => showPage("home")} className={page === "home" ? "nav-link active" : "nav-link"}>Home</button></li>
            <li><button onClick={() => showPage("transcription")} className={page === "transcription" ? "nav-link active" : "nav-link"}>Transcription</button></li>
            <li><button onClick={() => showPage("segments")} className={page === "segments" ? "nav-link active" : "nav-link"}>Segments</button></li>
            <li><button onClick={() => showPage("quality")} className={page === "quality" ? "nav-link active" : "nav-link"}>Quality</button></li>
            <li><button onClick={() => showPage("topic-search")} className={page === "topic-search" ? "nav-link active" : "nav-link"}>Topic Search</button></li>
            <li><button onClick={() => showPage("downloads")} className={page === "downloads" ? "nav-link active" : "nav-link"}>Downloads</button></li>
            <li><button onClick={clearResults} className="clear-btn">Clear Results</button></li>
          </ul>
        </div>
      </nav>

      {page === "home" && (
        <div id="home" className="page active">
          <div className="hero">
            <h1>MedicalPodcastAI</h1>
            <p>Navigate Medical Audio Content Efficiently</p>
            <p style={{ opacity: 0.7, fontSize: "1em" }}>AI-powered medical podcast analysis with transcription, segmentation & quality evaluation</p>
            
            <div className="upload-zone" onClick={() => !uploading && fileInputRef.current?.click()}>
              <input type="file" ref={fileInputRef} accept="audio/*" style={{ display: "none" }} onChange={handleFileUpload} disabled={uploading} />
              <div className="upload-icon">🎙️</div>
              <h2>Drop your medical audio here</h2>
              <p>or click to browse (supports large files)</p>
              {uploading && (
                <>
                  <div className="loader"></div>
                  <div className="progress-bar">
                    <div className="progress-fill" style={{ width: `${progress}%` }} />
                  </div>
                  <p>Processing medical audio… please wait</p>
                </>
              )}
              {currentFile && !uploading && (
                <div className="file-info">
                  <strong>File:</strong> {currentFile.name}<br />
                  <strong>Size:</strong> {formatFileSize(currentFile.size)}<br />
                  <strong>Type:</strong> {currentFile.type || "Unknown"}<br />
                  <strong>Last Modified:</strong> {new Date(currentFile.lastModified).toLocaleString()}
                </div>
              )}
            </div>

            <div className="progress-container">
              <div className="progress-steps">
                <div className="step active">
                  <div className="step-circle">🎧</div>
                  <p>Audio</p>
                </div>
                <div className={processedData ? "step active" : "step"}>
                  <div className="step-circle">📝</div>
                  <p>Transcript</p>
                </div>
                <div className={processedData ? "step active" : "step"}>
                  <div className="step-circle">🧩</div>
                  <p>Segments</p>
                </div>
                <div className={quality ? "step active" : "step"}>
                  <div className="step-circle">✅</div>
                  <p>Quality</p>
                </div>
                <div className="step active">
                  <div className="step-circle">🔍</div>
                  <p>Topics</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {page === "transcription" && (
        <div id="transcription" className="page active">
          <div className="transcription-container">
            <div className="transcript-text">
              <h3>Transcript</h3>
              <div dangerouslySetInnerHTML={{ 
                __html: processedData?.transcript 
                  ? highlightMedicalTerms(processedData.transcript) 
                  : "<p>Upload an audio file to see transcript...</p>" 
              }} />
            </div>
          </div>
        </div>
      )}

      {page === "quality" && (
        <div id="quality" className="page active">
          <h2 style={{ textAlign: "center", marginBottom: "40px" }}>Quality Evaluation Dashboard</h2>
          {quality ? (
            <div className="metrics-grid">
              <div className="metric-card">
                <h3>Accuracy & Error Rates</h3>
                <div style={{ height: '300px', position: 'relative' }}>
                  <Bar data={barData} options={chartOptions} />
                </div>
              </div>
              <div className="metric-card">
                <h3>WER Trend (Illustrative)</h3>
                <div style={{ height: '300px', position: 'relative' }}>
                  <Line data={lineData} options={chartOptions} />
                </div>
              </div>
              <div className="metric-card">
                <h3>Semantic Similarity</h3>
                <div style={{ height: '300px', position: 'relative' }}>
                  <Doughnut data={doughnutData} options={{...chartOptions, scales: undefined}} />
                </div>
              </div>
              <div className="metric-card">
                 <h3>All Metrics</h3>
                 <div className="metric-value-container">
                    <div className="metric-value-item">
                        <span className="metric-label">Accuracy</span>
                        <span className="metric-value">{quality.avg_accuracy}%</span>
                    </div>
                    <div className="metric-value-item">
                        <span className="metric-label">WER</span>
                        <span className="metric-value">{quality.avg_wer}%</span>
                    </div>
                    <div className="metric-value-item">
                        <span className="metric-label">CER</span>
                        <span className="metric-value">{quality.avg_cer}%</span>
                    </div>
                    <div className="metric-value-item">
                        <span className="metric-label">Similarity</span>
                        <span className="metric-value">{quality.avg_similarity}</span>
                    </div>
                 </div>
              </div>
            </div>
          ) : (
            <div className="glass-card" style={{ textAlign: "center", padding: "40px" }}>
              <i className="fas fa-exclamation-triangle" style={{ fontSize: "40px", marginBottom: "20px", color: "var(--accent)" }}></i>
              <p>Quality data not available. Please upload and process a file first.</p>
            </div>
          )}
        </div>
      )}

      {page === "segments" && (
        <div id="segments" className="page active">
          <h2 style={{ textAlign: "center", marginBottom: "40px" }}>Medical Segments</h2>
          <div className="segments-container">
            {processedData?.segments && Array.isArray(processedData.segments) ? (
              processedData.segments.map((segment, index) => (
                <div key={index} className="segment-card">
                  <div className="segment-header">
                    <span className="segment-label">{segment.segment_label || `Segment ${index + 1}`}</span>
                    <span className="segment-timestamp">{segment.start_time || ""} - {segment.end_time || ""}</span>
                  </div>
                  <p>{segment.segment_summary || (segment.segment_text || "").substring(0, 150)}</p>
                  <div className="keyword-tags">
                    {(segment.keywords || []).map((keyword, i) => (
                      <span key={i} className="keyword-tag">{keyword}</span>
                    ))}
                  </div>
                </div>
              ))
            ) : (
              <div className="glass-card" style={{ textAlign: "center", padding: "40px" }}>
                <i className="fas fa-file-audio" style={{ fontSize: "40px", marginBottom: "20px", color: "var(--primary)" }}></i>
                <p>Upload an audio file to see segments...</p>
              </div>
            )}
          </div>
        </div>
      )}

      {page === "topic-search" && (
        <div id="topic-search" className="page active">
          <h2 style={{ textAlign: "center", marginBottom: "40px" }}>Find Medical Topics</h2>
          <div className="topic-search-container">
            <div className="glass-card">
              <div className="search-input-container">
                <input 
                  className="search-input" 
                  placeholder="Type keyword (e.g. fever, anxiety, pneumonia)" 
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onKeyDown={handleSearchKeyPress}
                  disabled={uploading}
                />
                <button className="search-btn" onClick={searchTopic} disabled={uploading}>
                  <i className="fas fa-search"></i> Search
                </button>
              </div>
            </div>
            
            <div className="search-results">
              {searchMessage && (
                <div className="glass-card" style={{ textAlign: "center", padding: "40px" }}>
                  <i className="fas fa-search-minus" style={{ fontSize: "40px", marginBottom: "20px", color: "var(--accent)" }}></i>
                  <p>{searchMessage}</p>
                </div>
              )}
              {searchResults.map((seg, i) => (
                <div key={i} className="result-card">
                  <div className="result-header">
                    <span className="result-label">{seg.segment_label}</span>
                    <span className="result-timestamp">{seg.start_time || ""} - {seg.end_time || ""}</span>
                  </div>
                  <div 
                    className="result-text" 
                    dangerouslySetInnerHTML={{ 
                      __html: highlightSearchTerm(seg.segment_summary || seg.segment_text || "", searchQuery) 
                    }} 
                  />
                  <div className="result-keywords">
                    {(seg.keywords || []).map((k, j) => (
                      <span 
                        key={j} 
                        className="keyword-tag clickable" 
                        onClick={() => {
                          setSearchQuery(k);
                          setTimeout(searchTopic, 0);
                        }}
                      >
                        {k}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {page === "downloads" && (
        <div id="downloads" className="page active">
          <h2 style={{ textAlign: "center", marginBottom: "40px" }}>Export & Reports</h2>
          <div className="downloads-grid">
            {/* --- FIX: Replaced <a> with <button> for downloads --- */}
            <button className="download-card" onClick={() => !uploading && downloadFile("transcript")}>
              <div className="download-icon">📄</div>
              <h3>Transcript</h3>
              <p>Download full transcript in .txt format</p>
              <div className="download-btn">Download TXT</div>
            </button>
            
            <button className="download-card" onClick={() => !uploading && downloadFile("segments")}>
              <div className="download-icon">🧩</div>
              <h3>Segments</h3>
              <p>Download segmented data in .json format</p>
              <div className="download-btn">Download JSON</div>
            </button>
            
            <button className="download-card" onClick={() => !uploading && downloadFile("keywords")}>
              <div className="download-icon">🏷️</div>
              <h3>Keywords</h3>
              <p>Extract keywords in text format</p>
              <div className="download-btn">Download TXT</div>
            </button>
            
            <button className="download-card" onClick={() => !uploading && downloadFile("quality")}>
              <div className="download-icon">📊</div>
              <h3>Quality Report</h3>
              <p>Quality evaluation report</p>
              <div className="download-btn">Download TXT</div>
            </button>
            
            <button className="download-card" onClick={() => !uploading && downloadFile("summary")}>
              <div className="download-icon">📋</div>
              <h3>Summary</h3>
              <p>AI-generated medical summary</p>
              <div className="download-btn">Download TXT</div>
            </button>
            
            <button className="download-card" onClick={() => !uploading && downloadFile("all")}>
              <div className="download-icon">📦</div>
              <h3>Complete Package</h3>
              <p>All outputs combined</p>
              <div className="download-btn">Download TXT</div>
            </button>
          </div>
        </div>
      )}

      {notification.show && (
        <div 
          className={`notification ${notification.type}`}
          style={{
            position: "fixed",
            bottom: "20px",
            right: "20px",
            background: notification.type === "error" 
              ? "linear-gradient(135deg, #ff4444, #cc0000)" 
              : "linear-gradient(135deg, var(--primary), var(--secondary))",
            color: "white",
            padding: "15px 25px",
            borderRadius: "10px",
            boxShadow: "0 10px 30px rgba(0, 212, 255, 0.4)",
            zIndex: "10000",
            animation: "slideIn 0.3s ease",
          }}
        >
          {notification.message}
        </div>
      )}
    </>
  );
}