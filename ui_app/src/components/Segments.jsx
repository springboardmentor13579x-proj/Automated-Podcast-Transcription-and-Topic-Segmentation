import React from 'react';

const Segments = ({ processedData }) => {
  const segments = processedData?.segments || [];

  return (
    <div id="segments" className="page">
      <h2 style={{ textAlign: 'center', marginBottom: '40px' }}>
        Medical Segments
      </h2>

      <div className="segments-container">
        {segments.length > 0 ? (
          segments.map((segment, index) => (
            <div key={`${segment.label || 'seg'}-${index}`} className="segment-card">
              <div className="segment-header">
                <span className="segment-label">
                  {segment.label || `Segment ${index + 1}`}
                </span>
                <span className="segment-timestamp">
                  {segment.timestamp || ''}
                </span>
              </div>

              <p>
                {segment.summary ||
                  segment.text?.substring(0, 150) ||
                  'No description available'}
              </p>

              <div className="keyword-tags">
                {(segment.keywords || []).map((keyword, idx) => (
                  <span key={idx} className="keyword-tag">
                    {keyword}
                  </span>
                ))}
              </div>
            </div>
          ))
        ) : (
          <div
            className="glass-card"
            style={{ textAlign: 'center', padding: '40px' }}
          >
            <i
              className="fas fa-file-audio"
              style={{
                fontSize: '40px',
                marginBottom: '20px',
                color: 'var(--primary)'
              }}
            ></i>
            <p>Upload an audio file to see segments...</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Segments;
