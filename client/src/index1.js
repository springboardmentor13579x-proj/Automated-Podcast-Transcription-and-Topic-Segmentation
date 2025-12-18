import 'bootstrap/dist/css/bootstrap.min.css';
import { useState, useEffect } from 'react';

function App() {
  const [podcastData, setPodcastData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch data from your Python backend
  useEffect(() => {
    fetch('http://localhost:5000/api/summary')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        // If the Python server returns a list, set it directly
        // If it returns { filename: "...", topics: [...] }, access .topics
        const topics = Array.isArray(data) ? data : data.topics || [];
        setPodcastData(topics);
        setLoading(false);
      })
      .catch(error => {
        console.error("Error fetching data:", error);
        setError("Could not connect to Python. Is server.py running?");
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="text-center mt-5"><h3>⏳ Loading Summary...</h3></div>;
  if (error) return <div className="text-center mt-5 text-danger"><h3>❌ {error}</h3></div>;

  return (
    <div className="container mt-5">
      <header className="text-center mb-5">
        <h1 className="display-4 fw-bold text-primary">🎙️ Podcast Insights</h1>
        <p className="lead text-secondary">AI-Generated Summaries & Topic Segmentation</p>
      </header>

      {/* Check if data exists before mapping */}
      {podcastData.length === 0 ? (
        <div className="alert alert-warning text-center">No topics found in the data.</div>
      ) : (
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
                <div className="card-footer bg-white border-0">
                  <small className="text-muted">Snippet: "{topic.full_text_snippet}"</small>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;