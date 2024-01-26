import sys

from loguru import logger

# Configure the logger to output to console with a specific format
logger.remove()  # Remove default handler
logger.add(sys.stdout, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")

# Export the configured logger instance
__all__ = ['logger']
