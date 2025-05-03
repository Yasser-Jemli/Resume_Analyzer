# -*- coding: utf-8 -*-
# @Time    : 2023/10/12 16:00
# @Author  : Yasser JEMLI
# @File    : singleton_logger.py
# @Software: Vscode
# @Description: This module provides a singleton logger for the CV_PARSER_MODEL application.

import logging
import os
from pathlib import Path
from datetime import datetime
import shutil
from functools import wraps

class SingletonLogger:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SingletonLogger, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not SingletonLogger._initialized:
            self.cache_dir = Path(__file__).parent.parent / 'cache'
            self.debug_mode = False
            self.setup_cache_directory()
            self.setup_logging()
            SingletonLogger._initialized = True

    def set_debug_mode(self, enabled=True):
        """Enable or disable debug mode"""
        self.debug_mode = enabled
        if enabled:
            self.console_handler.setLevel(logging.DEBUG)
        else:
            self.console_handler.setLevel(logging.INFO)

    def setup_cache_directory(self):
        """Setup and clear cache directory"""
        if self.cache_dir.exists():
            shutil.rmtree(self.cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def setup_logging(self):
        """Configure logging with file and console handlers"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.log_file = self.cache_dir / f'resume_parser_{timestamp}.log'
        
        # Create root logger
        self.logger = logging.getLogger('ResumeParser')
        self.logger.setLevel(logging.DEBUG)
        
        # Remove existing handlers if any
        self.logger.handlers = []
        
        # File handler - always logs everything
        file_handler = logging.FileHandler(str(self.log_file))
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # Console handler - level depends on debug mode
        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(levelname)s - %(message)s')
        self.console_handler.setFormatter(console_formatter)
        self.logger.addHandler(self.console_handler)

    def get_logger(self, name=None):
        """Get a logger instance with optional custom name"""
        if name:
            logger = logging.getLogger(f'ResumeParser.{name}')
        else:
            logger = self.logger
        return logger

    @staticmethod
    def log_method(func):
        """Decorator to log method entry and exit"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = SingletonLogger().get_logger()
            logger.debug(f"Entering {func.__name__}")
            try:
                result = func(*args, **kwargs)
                logger.debug(f"Exiting {func.__name__}")
                return result
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {str(e)}")
                raise
        return wrapper
