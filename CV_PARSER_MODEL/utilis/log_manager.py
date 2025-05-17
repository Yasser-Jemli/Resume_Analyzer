import getpass  # To get the current user
import logging
import os
import platform
import subprocess
import sys
from datetime import datetime
from time import sleep


def ensure_psutil_installed():
    """Ensure that the `psutil` package is installed."""
    try:
        global psutil
        import psutil
    except ImportError:
        print("psutil not found. Attempting to install...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
        sleep(5)  # Wait for installation to complete
        try:
            import psutil
        except ImportError:
            raise RuntimeError("Failed to install psutil. Please install it manually.")


class LogManager:
    _instance = None  # Class-level variable to store the singleton instance

    def __new__(cls, *args, **kwargs):
        """Override the __new__ method to implement singleton behavior."""
        if cls._instance is None:
            cls._instance = super(LogManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize and configure the logging system."""
        # Check if already initialized to avoid re-initialization on subsequent calls
        if hasattr(self, "_initialized") and self._initialized:
            return

        # Construct the log directory by moving three levels up from the current script's directory
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.log_directory = os.path.join(base_dir, ".app_cache", "logs")

        self.ensure_log_directory_exists()

        # Create a new log file every time the app starts
        log_filename = self.create_new_log_file()
        self.write_log_header(log_filename)  # Write the custom header
        self.setup_logging(log_filename)

        # Mark as initialized to avoid re-initialization
        self._initialized = True

    def ensure_log_directory_exists(self):
        """Ensure that the log directory exists."""
        if not os.path.exists(self.log_directory):
            os.makedirs(self.log_directory)

    def create_new_log_file(self):
        """Create a new log file with a timestamp in the filename."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_filename = f"app_log_{timestamp}.log"
        log_filepath = os.path.join(self.log_directory, log_filename)
        return log_filepath

    def write_log_header(self, log_filepath):
        """Write a custom header to the log file."""
        with open(log_filepath, "w") as log_file:
            log_file.write("===== Application Log File =====\n")
            log_file.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            log_file.write(
                f"Operating System: {platform.system()} {platform.release()} ({platform.version()})\n"
            )
            log_file.write(
                f"Python Branch / Build / Compiler / Version :\n"
                f"  Branch: {platform.python_branch()}\n"
                f"  Build: {platform.python_build()}\n"
                f"  Compiler: {platform.python_compiler()}\n"
            )
            log_file.write(f"Python Version : {platform.python_version()}\n")
            log_file.write(f"Sys_Uname : {platform.uname()}\n")
            log_file.write(f"User: {getpass.getuser()}\n")
            log_file.write("=================================\n\n")
            log_file.write("=========== PC performance ===============\n")
            sys_info = self.get_system_info()

            # Format the system information dictionary into a readable string
            for key, value in sys_info.items():
                log_file.write(f"{key}: {value}\n")

            log_file.write("==========================================\n")

    def setup_logging(self, log_filepath):
        """Set up the logging configuration."""
        logging.basicConfig(
            filename=log_filepath,
            level=logging.DEBUG,  # Set the logging level
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Also log to console for debugging
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(
            logging.Formatter("%(name)s - %(levelname)s - %(message)s")
        )
        logging.getLogger().addHandler(console_handler)

    def get_system_info(self):
        """Retrieve system performance and hardware information."""
        ensure_psutil_installed()  # Ensure psutil is available
        system_info = {
            "CPU Usage (%)": psutil.cpu_percent(interval=1),
            "RAM Usage (%)": psutil.virtual_memory().percent,
            "Total RAM (GB)": round(psutil.virtual_memory().total / (1024 ** 3), 2),
            "Available RAM (GB)": round(
                psutil.virtual_memory().available / (1024 ** 3), 2
            ),
            "System Platform": platform.system(),
            "Platform Version": platform.version(),
            "Machine": platform.machine(),
            "Node": platform.node(),
            "Processor": platform.processor(),
            "Boot Time": datetime.fromtimestamp(psutil.boot_time()).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "Current Directory": os.getcwd(),
        }
        return system_info

    def log_matching_results(self, fully_matched, partially_matched, no_matching):
        logger = self.get_logger("MatchingResultsLogger")
        logger.info("Fully Matched Results:")
        for config_file, items in fully_matched.items():
            logger.info(f"{config_file}: {items}")

        logger.info("Partially Matched Results:")
        for config_file, items in partially_matched.items():
            logger.info(f"{config_file}: {items}")

        logger.info("No Matching Results:")
        for config_file, items in no_matching.items():
            logger.info(f"{config_file}: {items}")

    @classmethod
    def get_log_manager(cls):
        """Return the singleton instance of the LogManager."""
        if cls._instance is None:
            cls._instance = LogManager()
        return cls._instance

    def get_logger(self, name):
        """Return a logger instance with the given name."""
        return logging.getLogger(name)