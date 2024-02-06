import os
import logging
from fastapi import FastAPI, Request
from uvicorn import Config, Server
from contextlib import asynccontextmanager
from db.redis_wrapper import RedisClientWrapper
from scheduler.scheduler_wrapper import SchedulerWrapper  # Adjusted import


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    # Startup
    logging.info("Initializing resources")

    # Initialize and connect Redis client
    redis_wrapper = RedisClientWrapper()
    await redis_wrapper.connect(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        db=int(os.getenv("REDIS_DB", 0)),
        clear_on_startup=bool(os.getenv("REDIS_CLEAR_ON_STARTUP", False))
    )
    app.state.redis_wrapper = redis_wrapper

    # Initialize scheduler with Redis client
    app.state.scheduler_wrapper = SchedulerWrapper(
        redis_wrapper=redis_wrapper, start=True)

    yield

    # Shutdown
    await app.state.redis_wrapper.disconnect()
    if app.state.scheduler_wrapper.scheduler.running:
        app.state.scheduler_wrapper.scheduler.shutdown()
    logging.info("Resources have been cleaned up")


app = FastAPI(lifespan=lifespan)


async def run_server() -> None:
    logging.info('Application started')
    config = Config(
        app=app,
        host=os.getenv("SERVER_HOST", "localhost"),
        port=int(os.getenv("SERVER_PORT", 8000)),
    )
    server = Server(config)
    await server.serve()


@app.get("/start-scheduler")
async def start_scheduler(request: Request):
    scheduler = request.app.state.scheduler_wrapper.scheduler
    if not scheduler.running:
        scheduler.start()
        return {"message": "Scheduler started and jobs scheduled."}
    return {"message": "Scheduler is already running."}


@app.get("/stop-scheduler")
async def stop_scheduler(request: Request):
    scheduler = request.app.state.scheduler_wrapper.scheduler
    if scheduler.running:
        scheduler.shutdown()
        return {"message": "Scheduler stopped."}
    return {"message": "Scheduler is not running."}
