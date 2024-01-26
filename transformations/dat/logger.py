from loguru import logger

# Configure the logger with appropriate settings
logger.remove()  # Remove default handlers
logger.add(
    "transformations/logs/transformations.log",  # Log output file
    rotation="10 MB",  # New file is created each time the current log file reaches 10 MB
    retention="10 days",  # Retain log files for 10 days
    level="INFO",  # Log level set to INFO
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",  # Log message format
    backtrace=True,  # Include the traceback of the exception
    diagnose=True  # Include variable values in the traceback
)
