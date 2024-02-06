import os
import logging
from fastapi import FastAPI
from uvicorn import Config, Server
from contextlib import asynccontextmanager
from db.redis_wrapper import RedisClientWrapper
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

    redis_client = RedisClientWrapper()
    await redis_client.connect(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        db=int(os.getenv("REDIS_DB", 0)),
    )
    app.state.redis_client = redis_client

    yield
    # Shutdown
    await app.state.redis_client.disconnect()
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
