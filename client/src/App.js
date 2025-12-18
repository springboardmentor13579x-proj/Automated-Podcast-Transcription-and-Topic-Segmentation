import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css'; // Import Bootstrap styles
import podcastData from './data.json'; // Import your JSON data

function App() {
  return (
    <div className="container mt-5">
      {/* Header Section */}
      <header className="text-center mb-5">
        <h1 className="display-4 fw-bold text-primary">🎙️ Podcast Insights</h1>
        <p className="lead text-secondary">
          AI-Generated Summaries & Topic Segmentation
        </p>
      </header>

      {/* Topics Grid */}
      <div className="row">
        {podcastData.map((topic, index) => (
          <div className="col-md-6 mb-4" key={index}>
            <div className="card h-100 shadow-sm border-0">
              <div className="card-body">
                
                {/* Topic Header */}
                <div className="d-flex justify-content-between align-items-center mb-3">
                  <h5 className="card-title fw-bold text-dark">
                    Topic {topic.topic_id}
                  </h5>
                  <span className="badge bg-secondary">
                    {topic.keywords.length} Keywords
                  </span>
                </div>

                {/* Keywords (Tags) */}
                <div className="mb-3">
                  {topic.keywords.map((keyword, kIndex) => (
                    <span 
                      key={kIndex} 
                      className="badge bg-light text-primary border me-1"
                    >
                      #{keyword}
                    </span>
                  ))}
                </div>

                {/* Summary Text */}
                <p className="card-text text-muted">
                  {topic.summary}
                </p>
              </div>
              
              {/* Footer with "Read More" dummy link */}
              <div className="card-footer bg-white border-0">
                <small className="text-muted">
                   Snippet: "{topic.full_text_snippet}"
                </small>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;