import React from 'react';
import { API } from '../api';

const Downloads = ({ processedData, showNotification }) => {
  const downloadFile = async (type) => {
    if (!processedData) {
      showNotification('Please upload an audio file first', 'error');
      return;
    }

    let content = '';
    let filename = '';

    switch (type) {
      case 'transcript':
        content = processedData.transcript;
        filename = 'transcript.txt';
        break;

      case 'segments':
        content = JSON.stringify(processedData.segments, null, 2);
        filename = 'segments.json';
        break;

      case 'quality':
        const res = await fetch(`${API}/quality`);
        const data = await res.json();
        content = JSON.stringify(data, null, 2);
        filename = 'quality.json';
        break;

      default:
        return;
    }

    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();

    URL.revokeObjectURL(url);
  };

  return (
    <div className="page">
      <h2>Downloads</h2>

      <button onClick={() => downloadFile('transcript')}>
        Download Transcript
      </button>

      <button onClick={() => downloadFile('segments')}>
        Download Segments
      </button>

      <button onClick={() => downloadFile('quality')}>
        Download Quality
      </button>
    </div>
  );
};

export default Downloads;
