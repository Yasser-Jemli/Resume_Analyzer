# -*- coding: utf-8 -*-
# @Time    : 2023/10/12 16:00
# @Author  : Yasser JEMLI
# @File    : singleton_logger.py
# @Software: Vscode
# @Description: This module provides a singleton logger for the CV_PARSER_MODEL application.

import logging
import threading

class SingletonLogger:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, name="ResumeAnalyzerLogger", log_file=None, level=logging.DEBUG):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(SingletonLogger, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self, name="ResumeAnalyzerLogger", log_file=None, level=logging.DEBUG):
        if self._initialized:
            return
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # File Handler (optional)
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        self._initialized = True

    def get_logger(self):
        return self.logger
