import logging

def setup_logger():
    logger = logging.getLogger('grading_logger')
    if not logger.hasHandlers():  # Check if the logger already has handlers
        handler = logging.FileHandler('Logs/grading.log')
        handler.setLevel(logging.DEBUG)  # Use DEBUG to capture all logs
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    return logger