import asyncio
import os
import sys
import logging
import setup_env
from scheduler import scheduler
from server import run_server
# from twitter.twitter_client import twitter_client
# from openai.openai_llm_chains import llm_chains


async def main() -> None:
    scheduler.start()
    await run_server()

# Run
if __name__ == "__main__":
    try:
        logging.info("Application running - Press Ctrl+C to exit.")
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Application interrupted. Shutting down gracefully...")
        sys.exit(0)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)
    finally:
        logging.info("Application has been shut down")
        sys.exit(0)
