import React, { useState } from 'react';

const TopicSearch = ({ processedData, showNotification }) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  const handleSearch = () => {
    if (!query.trim()) {
      setResults([]);
      return;
    }

    if (!processedData || !processedData.segments) {
      showNotification('Please upload an audio file first', 'error');
      return;
    }

    const q = query.toLowerCase();

    const matches = processedData.segments.filter(seg =>
      (seg.text && seg.text.toLowerCase().includes(q)) ||
      (seg.summary && seg.summary.toLowerCase().includes(q)) ||
      (seg.keywords || []).some(k => k.toLowerCase().includes(q))
    );

    setResults(matches);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') handleSearch();
  };

  const highlight = (text = '') => {
    const regex = new RegExp(`(${query})`, 'gi');
    return text.replace(
      regex,
      '<span style="background: rgba(0, 212, 255, 0.3); padding: 2px 4px; border-radius: 4px;">$1</span>'
    );
  };

  return (
    <div id="topic-search" className="page">
      <h2 style={{ textAlign: 'center', marginBottom: '40px' }}>
        Find Medical Topics
      </h2>

      <div className="topic-search-container">
        <div className="glass-card">
          <div className="search-input-container">
            <input
              className="search-input"
              placeholder="Type keyword (e.g. fever, anxiety, pneumonia)"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={handleKeyPress}
            />
            <button className="search-btn" onClick={handleSearch}>
              <i className="fas fa-search"></i> Search
            </button>
          </div>
        </div>

        <div className="search-results">
          {!query && (
            <div className="glass-card" style={{ textAlign: 'center', padding: '40px' }}>
              <i className="fas fa-search" style={{ fontSize: '40px', marginBottom: '20px', color: 'var(--primary)' }}></i>
              <p>Enter a medical topic to search for relevant segments.</p>
            </div>
          )}

          {query && results.length === 0 && (
            <div className="glass-card" style={{ textAlign: 'center', padding: '40px' }}>
              <i className="fas fa-search-minus" style={{ fontSize: '40px', marginBottom: '20px', color: 'var(--accent)' }}></i>
              <p>No matching topic found for "{query}".</p>
            </div>
          )}

          {results.length > 0 && (
            <div>
              <h3 style={{ marginBottom: '20px' }}>
                Found {results.length} matching segment(s)
              </h3>

              {results.map((seg, index) => (
                <div key={index} className="result-card">
                  <div className="result-header">
                    <span className="result-label">
                      {seg.label || `Segment ${index + 1}`}
                    </span>
                    <span className="result-timestamp">
                      {seg.timestamp || ''}
                    </span>
                  </div>

                  <div
                    className="result-text"
                    dangerouslySetInnerHTML={{
                      __html: highlight(seg.summary || seg.text || '')
                    }}
                  />

                  <div className="result-keywords">
                    {(seg.keywords || []).map((k, idx) => (
                      <span key={idx} className="keyword-tag">
                        {k}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default TopicSearch;
