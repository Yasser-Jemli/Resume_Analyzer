import logging

class VerifyState:
    def run(self, publisher_success, logger_success):
        logging.info("Verifying State 2 processes...")
        return publisher_success and logger_success