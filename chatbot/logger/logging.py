import os
import sys
import logging
from datetime import datetime

# Format the datetime to a string suitable for filenames
LOG_FILE = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"

# Example usage in logging setup (if you're setting up a log file):
log_file_path = os.path.join(os.getcwd(), "logs")

# Make the directory if it doesn't exist
os.makedirs(log_file_path, exist_ok=True)

# Combine the log directory path with the log file name
LOG_FILE_PATH = os.path.join(log_file_path, LOG_FILE)

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    filename=LOG_FILE_PATH,
    format="%(asctime)s - %(levelname)s - %(message)s - %(module)s - Line: %(lineno)d"
)

# Example log messages to check logging functionality
logging.info("This is an info message.")
logging.error("This is an error message.")
