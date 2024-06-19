"""
Default configuration for the logging
can be further configured inside other modules
"""

import logging

# Setting file handler, configured for only errors
logger = logging.getLogger(__name__)

# Setting formatter
formatter = logging.Formatter(
    "%(asctime)s->%(name)s:%(levelname)s:%(message)s"
)

logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(
    filename="./backing-pet/logs/errors.log", mode="+a")
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)

# Setting Stream handler, configured for debugging and info messages
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


# Testing configurations if run here
if __name__ == "__main__":
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
