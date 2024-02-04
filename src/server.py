import logging
from uvicorn import Config, Server

from redis_conn import create_redis_connection
import os
import logging
from redis_conn import create_redis_connection
from fastapi import FastAPI
from redis_conn import create_redis_connection
from uvicorn import Config, Server
from contextlib import asynccontextmanager


async def run_server() -> None:
    logging.info(f'Application started')

    config = Config(
        app=app,
        host=os.getenv("SERVER_HOST", "localhost"),
        port=int(os.getenv("SERVER_PORT", 8000))
    )
    server = Server(config)
    await server.serve()


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    # Startup
    logging.info("Initializing resources")

    app.state.redis_client = await create_redis_connection(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        db=int(os.getenv("REDIS_DB", 0)),
    )

    yield
    # Shutdown
    await app.state.redis_client.aclose()
    logging.info("Resources have been cleaned up")


app = FastAPI(lifespan=lifespan)
