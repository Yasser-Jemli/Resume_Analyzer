from .logger import SingletonLogger

# Global logger instance
_logger = SingletonLogger()

def get_logger(name=None):
    """Get a logger instance"""
    return _logger.get_logger(name)

def set_debug_mode(enabled=True):
    """Enable or disable debug mode"""
    _logger.set_debug_mode(enabled)

def log_method(func):
    """Method logging decorator"""
    return SingletonLogger.log_method(func)

# from utilis.log import get_logger, log_method

# logger = get_logger(__name__)

# class ResumeInfoExtractor:
#     @log_method
#     def extract_all(self):
#         logger.info("Starting resume extraction")
#         try:
#             # Your code here
#             logger.debug("Processing details...")
#             results = {...}
#             logger.info("Extraction completed successfully")
#             return results
#         except Exception as e:
#             logger.error(f"Extraction failed: {str(e)}")
#             raise