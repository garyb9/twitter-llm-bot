import os
import logging
from dotenv import load_dotenv
import random
import time

# Setup environment
load_dotenv(
    dotenv_path=os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../.env'))
)

# Set up logger
logging.basicConfig(
    format='%(asctime)s:%(msecs)d\t%(name)s:\t%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
    # filename='app.log',  # Log file path
    # filemode='w',  # Append mode (use 'w' for overwrite mode)
)

# Seed the random number generator with the current system time
random.seed(time.time())