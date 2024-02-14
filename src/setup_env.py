import os
import logging
from dotenv import load_dotenv

# Setup
load_dotenv(
    dotenv_path=os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../.env'))
)

logging.basicConfig(
    format='%(asctime)s:%(msecs)d\t%(name)s:\t%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
    # filename='app.log',  # Log file path
    # filemode='w',  # Append mode (use 'w' for overwrite mode)
)