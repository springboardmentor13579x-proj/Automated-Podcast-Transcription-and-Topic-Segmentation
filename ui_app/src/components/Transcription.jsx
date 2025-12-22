import React, { useState, useEffect } from 'react';

const Transcription = ({ processedData, currentFile }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [audioDuration, setAudioDuration] = useState('--:--');
  const [fileSizeDisplay, setFileSizeDisplay] = useState('--');

  useEffect(() => {
    if (!currentFile) return;

    const formatFileSize = (bytes = 0) => {
      if (!bytes) return '0 Bytes';
      const k = 1024;
      const sizes = ['Bytes', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    };

    setFileSizeDisplay(formatFileSize(currentFile.size));

    const durationMinutes = Math.max(
      1,
      Math.round((currentFile.size / (1024 * 1024)) * 1.5)
    );

    setAudioDuration(
      `${String(Math.floor(durationMinutes / 60)).padStart(2, '0')}:${String(
        durationMinutes % 60
      ).padStart(2, '0')}`
    );
  }, [currentFile]);

  const highlightMedicalTerms = (text = '') => {
    const medicalTerms = [
      'pain', 'fever', 'chest', 'breath', 'anxiety', 'insomnia',
      'cardiac', 'vital', 'crackles', 'COVID-19', 'ECG', 'X-ray',
      'BP', 'blood pressure', 'heart rate', 'temperature', 'oxygen',
      'hypertension', 'diabetes', 'medications', 'dizziness', 'fatigue'
    ];

    let output = text;
    medicalTerms.forEach(term => {
      const regex = new RegExp(`\\b(${term})\\b`, 'gi');
      output = output.replace(
        regex,
        '<span class="medical-term">$1</span>'
      );
    });

    return output.replace(/\n/g, '<br/>');
  };

  const togglePlayback = () => {
    setIsPlaying(prev => !prev);
  };

  return (
    <div id="transcription" className="page">
      <div className="transcription-container">

        <div className="audio-player">
          <h3>Audio Player</h3>
          <div className="waveform"></div>

          <button className="send-btn" onClick={togglePlayback}>
            <i className={`fas fa-${isPlaying ? 'pause' : 'play'}`}></i>{' '}
            {isPlaying ? 'Pause' : 'Play'}
          </button>

          <div style={{ marginTop: '20px' }}>
            <p>Duration: <span>{audioDuration}</span></p>
            <p>File Size: <span>{fileSizeDisplay}</span></p>
          </div>
        </div>

        <div className="transcript-text">
          <h3>Transcript</h3>

          {!processedData || !processedData.transcript ? (
            <p>Upload an audio file to see transcript...</p>
          ) : (
            <div
              dangerouslySetInnerHTML={{
                __html: highlightMedicalTerms(processedData.transcript)
              }}
            />
          )}
        </div>

      </div>
    </div>
  );
};

export default Transcription;
