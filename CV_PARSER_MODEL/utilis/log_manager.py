import threading
from queue import Queue, Empty
import getpass
import logging
import os
import platform
import sys
from datetime import datetime
import time
import shutil
from pathlib import Path


class LogManager:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LogManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._log_queue = Queue()
        self._stop_event = threading.Event()

        # Initialize logging directory and cleanup old logs
        base_dir = Path(__file__).parent.parent
        self.log_directory = base_dir / ".app_cache" / "logs"
        self.cleanup_old_logs()
        self.setup_logging()

        # Start logging thread
        self._log_thread = threading.Thread(target=self._log_worker, daemon=True)
        self._log_thread.start()

        self._initialized = True

    def cleanup_old_logs(self):
        """Remove old log files and create new directory"""
        try:
            if self.log_directory.exists():
                shutil.rmtree(self.log_directory)
            self.log_directory.mkdir(parents=True, exist_ok=True)

        except Exception as e:
            print(f"Error cleaning up logs: {e}")

    def _log_worker(self):
        """Worker thread that processes log messages from the queue"""
        while not self._stop_event.is_set():
            try:
                record = self._log_queue.get(timeout=0.1)
                self._actual_log(record)
                self._log_queue.task_done()
            except Empty:
                continue
            except Exception as e:
                print(f"Error in log worker: {str(e)}")
                continue

    def setup_logging(self):
        """Configure logging with new file"""
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.log_file = self.log_directory / f'app_log_{timestamp}.log'

        # Configure handlers
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)

        # Root logger setup
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)

        # Remove any existing handlers
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        root_logger.addHandler(file_handler)

        # Write initial log header
        self.write_log_header()

    def configure_logging(self, file_logging=True, console_logging=True):
        """Configure logging with specified handlers"""
        # Remove all existing handlers
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # Set base configuration
        root_logger.setLevel(logging.DEBUG)
        
        if file_logging:
            # Clean up old logs first
            if self.log_directory.exists():
                shutil.rmtree(self.log_directory)
            self.log_directory.mkdir(parents=True, exist_ok=True)
            
            # File handler setup
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            log_file = self.log_directory / f'resume_parser_{timestamp}.log'
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            root_logger.addHandler(file_handler)
        
        if console_logging:
            # Console handler setup
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_formatter = logging.Formatter('%(levelname)s - %(message)s')
            console_handler.setFormatter(console_formatter)
            root_logger.addHandler(console_handler)
        
        # If neither logging type is enabled, add a null handler
        if not file_logging and not console_logging:
            root_logger.addHandler(logging.NullHandler())

    def write_log_header(self):
        """Write application header to log file"""
        with open(self.log_file, 'w') as f:
            f.write("===== Application Log File =====\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Operating System: {platform.platform()}\n")
            f.write("Python Branch / Build / Compiler / Version :\n")
            f.write(f"  Branch: {sys.version}\n")
            f.write(f"  Build: {sys.version_info}\n")
            f.write(f"  Compiler: {platform.python_compiler()}\n")
            f.write(f"Python Version : {platform.python_version()}\n")
            f.write(f"Sys_Uname : {os.uname()}\n")
            f.write(f"User: {getpass.getuser()}\n")
            f.write("="*33 + "\n\n")

    def queue_log(self, name, level, message):
        """Queue a log message"""
        if not self._stop_event.is_set():
            self._log_queue.put({
                'name': name,
                'level': level,
                'message': message
            })

    def _actual_log(self, record):
        """Process a log record"""
        logger = logging.getLogger(record['name'])

        if record['level'] == 'DEBUG':
            logger.debug(record['message'])
        elif record['level'] == 'INFO':
            logger.info(record['message'])
        elif record['level'] == 'WARNING':
            logger.warning(record['message'])
        elif record['level'] == 'ERROR':
            logger.error(record['message'])

    def get_logger(self, name):
        """Get a logger instance"""
        return ThreadedLogger(self, name)

    def shutdown(self):
        """Clean shutdown of logging thread"""
        self._stop_event.set()
        if self._log_thread.is_alive():
            self._log_thread.join(timeout=1.0)

    @classmethod
    def get_log_manager(cls):
        """Get or create the singleton instance"""
        if cls._instance is None:
            cls._instance = LogManager()
        return cls._instance


class ThreadedLogger:
    """Thread-safe logger proxy"""
    def __init__(self, manager, name):
        self.manager = manager
        self.name = name

    def debug(self, message):
        self.manager.queue_log(self.name, 'DEBUG', message)

    def info(self, message):
        self.manager.queue_log(self.name, 'INFO', message)

    def warning(self, message):
        self.manager.queue_log(self.name, 'WARNING', message)

    def error(self, message):
        self.manager.queue_log(self.name, 'ERROR', message)


def print_parser_results(results):
    """Pretty print parser results"""
    if not results:
        logger.error("No results available")
        return
        
    for key, value in results.items():
        if args.console:  # Only print if console output is enabled
            print(f"\n{key}:")
        logger.info(f"{key}:")
        if isinstance(value, list):
            for item in value:
                logger.info(f"-{item}")
                if args.console:
                    print(f"- {item}")
        else:
            if args.console:
                print(value)