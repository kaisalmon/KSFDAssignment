import logging
import sys


def setup_logging(verbose) -> logging.Logger:
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if verbose else logging.ERROR)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG if verbose else logging.ERROR)
    formatter = logging.Formatter('%(asctime)s - %(message)s', '%H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger