import sys
import logging

logger = logging.getLogger("inference_logger")
logger.setLevel(logging.DEBUG)  # Set to DEBUG to capture all logs

# Create a console handler for logging to stdout
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(
    logging.INFO
)  # Log level for console output (higher than DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
