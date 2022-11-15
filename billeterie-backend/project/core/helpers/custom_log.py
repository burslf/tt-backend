import logging


def get_logger():
    logger = logging.getLogger()
    logger.setLevel("INFO")
    return logger
