import logging
import os
from typing import Dict

class Logger:
    """Logger handler for the application"""
    
    def __init__(self, config: Dict):
        """Initialize logger with configuration"""
        self.logger = logging.getLogger('app')
        self.logger.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # Create file handler if log directory is specified
        log_dir = config.get('log_dir', 'logs')
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
            file_handler = logging.FileHandler(os.path.join(log_dir, 'app.log'))
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
            
    def info(self, message: str):
        """Log info message"""
        self.logger.info(message)
        
    def error(self, message: str):
        """Log error message"""
        self.logger.error(message)
        
    def warning(self, message: str):
        """Log warning message"""
        self.logger.warning(message)
        
    def debug(self, message: str):
        """Log debug message"""
        self.logger.debug(message) 