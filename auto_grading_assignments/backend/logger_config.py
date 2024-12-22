import logging, os

def setup_logger(file_name="grading"):
    logger = logging.getLogger(f'{file_name}_logger')
    if not logger.hasHandlers():  # Check if the logger already has handlers
        handler = logging.FileHandler(os.path.join('Logs',f'{file_name}.log'))
        handler.setLevel(logging.DEBUG)  # Use DEBUG to capture all logs
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    return logger