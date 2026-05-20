"""Logger configuration for the application."""
import logging
import logging.handlers
from config import Config


def setup_logger(name: str) -> logging.Logger:
    """Setup logger with file and console handlers.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(Config.LOG_LEVEL)
    
    # Create formatters
    formatter = logging.Formatter(Config.LOG_FORMAT)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(Config.LOG_LEVEL)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        Config.LOG_FILE,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(Config.LOG_LEVEL)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger
