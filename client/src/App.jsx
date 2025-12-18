import { useState } from 'react';

function App() {
  const [podcastData, setPodcastData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);

  // 1. Handle File Selection
  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  // 2. Upload and Process
  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Please select a file first!");
      return;
    }

    setLoading(true);
    setError(null);
    setPodcastData([]); // Clear old data

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      // Send file to Python
      const response = await fetch('http://localhost:5000/api/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Processing failed. Check server console.');
      }

      const data = await response.json();
      
      // Handle list or object format
      const topics = Array.isArray(data) ? data : data.topics || [];
      setPodcastData(topics);
      
    } catch (err) {
      console.error(err);
      setError("Error processing file. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-5">
      <header className="text-center mb-5">
        <h1 className="display-4 fw-bold text-primary">🎙️ Dynamic Podcast AI</h1>
        <p className="lead text-secondary">Upload an audio file to generate summaries instantly.</p>
      </header>

      {/* Upload Section */}
      <div className="card p-4 mb-5 shadow-sm bg-light">
        <div className="row align-items-center">
          <div className="col-md-8">
            <input 
              type="file" 
              className="form-control" 
              accept=".mp3,.wav" 
              onChange={handleFileChange} 
            />
          </div>
          <div className="col-md-4 text-end">
            <button 
              className="btn btn-primary w-100 fw-bold" 
              onClick={handleUpload} 
              disabled={loading}
            >
              {loading ? "⚙️ Processing..." : " Upload & Analyze"}
            </button>
          </div>
        </div>
        {loading && <div className="mt-3 text-muted text-center"><small>This may take 1-2 minutes. Please wait...</small></div>}
      </div>

      {/* Error Message */}
      {error && <div className="alert alert-danger text-center">{error}</div>}

      {/* Results Section */}
      <div className="row">
        {podcastData.map((topic, index) => (
          <div className="col-md-6 mb-4" key={index}>
            <div className="card h-100 shadow-sm border-0">
              <div className="card-body">
                <div className="d-flex justify-content-between align-items-center mb-3">
                  <h5 className="card-title fw-bold text-dark">Topic {topic.topic_id}</h5>
                  <span className="badge bg-secondary">{topic.keywords ? topic.keywords.length : 0} Keywords</span>
                </div>

                <div className="mb-3">
                  {topic.keywords && topic.keywords.map((keyword, kIndex) => (
                    <span key={kIndex} className="badge bg-light text-primary border me-1">
                      #{keyword}
                    </span>
                  ))}
                </div>

                <p className="card-text text-muted">{topic.summary}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;