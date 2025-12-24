// src/utils/logger.js

const sendLogToBackend = async (log) => {
  try {
    await fetch("http://localhost:5000/api/logs", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(log)
    });
  } catch (err) {
    console.error("Failed to send log to backend", err);
  }
};

const logger = {
  info: (message, data = {}) => {
    console.log("INFO:", message);
    sendLogToBackend({
      level: "info",
      message,
      data
    });
  },

  error: (message, data = {}) => {
    console.error("ERROR:", message);
    sendLogToBackend({
      level: "error",
      message,
      data
    });
  }
};

export default logger;
