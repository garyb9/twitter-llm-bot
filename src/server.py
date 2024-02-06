import logging
from uvicorn import Config, Server

from db.redis_conn import create_redis_connection
import os
import logging
from db.redis_conn import create_redis_connection
from fastapi import FastAPI
from db.redis_conn import create_redis_connection
from uvicorn import Config, Server
from contextlib import asynccontextmanager

from scheduler.scheduler import create_scheduler


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
scheduler = create_scheduler()


@app.get("/start-scheduler")
async def start_scheduler():
    if scheduler and not scheduler.running:
        scheduler.start()
        return {"message": "Scheduler started and jobs scheduled."}
    else:
        return {"message": "Scheduler is already running."}


@app.get("/stop-scheduler")
async def stop_scheduler():
    if scheduler and scheduler.running:
        scheduler.shutdown()
        return {"message": "Scheduler stopped."}
    else:
        return {"message": "Scheduler is not running."}
