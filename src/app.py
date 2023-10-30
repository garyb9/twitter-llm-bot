import os
import sys
import logging
import setup_env
from scheduler import scheduler
from server import app
from twitter_client import twitter_client
from openai_llm_chains import llm_chains

# Run
if __name__ == "__main__":
    try:
        scheduler.start()  # Start scheduler
        logging.info("Press Ctrl+C to exit.")
        app.run(port=int(os.getenv('PORT', 3000)))  # Run server
    except (KeyboardInterrupt, SystemExit):
        logging.info('Got SIGTERM! Terminating...')
        scheduler.shutdown()
        sys.exit(0)
