import logging
import sys
import os

def setup_logging(env: str = os.getenv("LOGGER")):
    if env is None:
        env = os.getenv('APP_ENV', 'dev')  # fallback to 'dev'

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # let handlers filter

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')

    if env == 'dev':
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
    elif env == 'test':
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
    elif env == 'prod':
        os.makedirs('logs', exist_ok=True)
        handler = logging.FileHandler('logs/production.log')
        handler.setLevel(logging.WARNING)
    else:
        raise ValueError(f"Unknown logging environment: {env}")

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
