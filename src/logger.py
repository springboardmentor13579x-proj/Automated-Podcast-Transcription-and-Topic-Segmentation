import logging
import os
import sys
import uuid
from datetime import datetime

# Constants
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)

class SessionLogger:
    """
    A context manager-like structure or singleton helper to manage logging sessions.
    However, standard python logging is best used with a setup function.
    """
    _current_session_id = None
    _current_log_file = None

    @staticmethod
    def output_log_file_path():
        return SessionLogger._current_log_file

    @staticmethod
    def start_new_session():
        """
        Initializes a new logging session.
        Returns the session_id and the log file path.
        """
        # Generate Session ID
        session_id = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:8]}"
        SessionLogger._current_session_id = session_id

        # Log File Name
        log_filename = f"session_{session_id}.log"
        log_filepath = os.path.join(LOGS_DIR, log_filename)
        SessionLogger._current_log_file = log_filepath

        # Configure Root Logger
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)

        # Clear existing handlers (important for Streamlit re-runs)
        if root_logger.hasHandlers():
            root_logger.handlers.clear()

        # Formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # File Handler
        file_handler = logging.FileHandler(log_filepath, encoding='utf-8')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        root_logger.addHandler(file_handler)

        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)
        root_logger.addHandler(console_handler)
        
        logging.info(f"New Session Started: {session_id}")
        return session_id, log_filepath

    @staticmethod
    def get_logger(name):
        return logging.getLogger(name)

def get_logger(name):
    """Refers to standard logging getLogger, wrapped for convenience if needed."""
    return logging.getLogger(name)
