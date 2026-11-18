import logging
import os

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "forensics.log")


def getForensicsLogger(name="kubesec.forensics"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(LOG_FILE)
        handler.setFormatter(logging.Formatter(
            "%(asctime)s | %(levelname)s | %(module)s.%(funcName)s | %(message)s"))
        logger.addHandler(handler)
        logger.propagate = False
    return logger