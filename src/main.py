import sys
import logging
import asyncio
import setup_env
from server import run_server


async def main() -> None:
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
