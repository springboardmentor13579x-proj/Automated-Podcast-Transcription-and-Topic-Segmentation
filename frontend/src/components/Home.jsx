import React, { useState, useRef, useEffect } from "react";
import { API } from "../api";

const Home = ({ setProcessedData, setCurrentFile, setCurrentPage, showNotification }) => {
  const [fileInfo, setFileInfo] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);
  const [showProgress, setShowProgress] = useState(false);

  const fileInputRef = useRef(null);
  const progressIntervalRef = useRef(null);

  useEffect(() => {
    return () => {
      if (progressIntervalRef.current) {
        clearInterval(progressIntervalRef.current);
      }
    };
  }, []);

  const formatFileSize = (bytes) => {
    if (!bytes) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return (bytes / Math.pow(k, i)).toFixed(2) + " " + sizes[i];
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setCurrentFile(file);

    setFileInfo({
      name: file.name,
      size: formatFileSize(file.size),
      type: file.type || "Unknown",
      lastModified: new Date(file.lastModified).toLocaleString(),
    });

    setIsUploading(true);
    setShowProgress(true);
    setUploadProgress(0);

    let progress = 0;
    progressIntervalRef.current = setInterval(() => {
      progress = Math.min(progress + 5, 90);
      setUploadProgress(progress);
    }, 800);

    try {
      const formData = new FormData();
      formData.append("audio", file);

      const response = await fetch(`${API}/upload`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Upload failed");
      }

      const resultData = await response.json();

      if (resultData.status !== "completed") {
        throw new Error("Processing failed");
      }

      //  STOP LOADER IMMEDIATELY AFTER TRANSCRIPTION
      clearInterval(progressIntervalRef.current);
      setUploadProgress(100);
      setIsUploading(false);
      setShowProgress(false);

      //  SAVE TRANSCRIPT & SEGMENTS
      setProcessedData({
        transcript: resultData.transcript,
        segments: resultData.segments,
        fileInfo: file,
      });

      setCurrentPage("transcription");
      showNotification("Transcript generated successfully!", "success");

    } catch (err) {
      clearInterval(progressIntervalRef.current);
      setIsUploading(false);
      setShowProgress(false);
      showNotification(err.message, "error");
    }
  };

  return (
    <div className="page">
      <div className="hero">
        <h1>MedicalPodcastAI</h1>
        <p>Navigate Medical Audio Content Efficiently</p>

        <div
          className="upload-zone"
          onClick={() => fileInputRef.current.click()}
        >
          <input
            type="file"
            ref={fileInputRef}
            accept="audio/*"
            hidden
            onChange={handleFileUpload}
          />

          <div className="upload-icon">🎙️</div>
          <h2>Drop your medical audio here</h2>
          <p>or click to browse</p>

          {showProgress && (
            <>
              <div className="progress-bar">
                <div
                  className="progress-fill"
                  style={{ width: `${uploadProgress}%` }}
                ></div>
              </div>
              <p>Processing…</p>
            </>
          )}

          {fileInfo && (
            <div className="file-info">
              <strong>File:</strong> {fileInfo.name}<br />
              <strong>Size:</strong> {fileInfo.size}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Home;
