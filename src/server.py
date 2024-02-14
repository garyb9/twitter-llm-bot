import os
import logging
from fastapi import FastAPI, Request
from uvicorn import Config, Server
from contextlib import asynccontextmanager
from db.redis_wrapper import RedisClientWrapper
from scheduler.jobs import TWEET_QUEUE
from scheduler.scheduler_wrapper import SchedulerWrapper  # Adjusted import


@asynccontextmanager
async def lifespan(app: FastAPI):
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
    app.state.scheduler_wrapper = SchedulerWrapper(redis_wrapper=redis_wrapper)

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


@app.post("/start-scheduler")
async def start_scheduler(request: Request):
    scheduler = request.app.state.scheduler_wrapper.scheduler
    if not scheduler.running:
        scheduler.start()
        return {"message": "Scheduler started and jobs scheduled."}
    return {"message": "Scheduler is already running."}


@app.post("/stop-scheduler")
async def stop_scheduler(request: Request):
    scheduler = request.app.state.scheduler_wrapper.scheduler
    if scheduler.running:
        scheduler.shutdown()
        return {"message": "Scheduler stopped."}
    return {"message": "Scheduler is not running."}


@app.get("/get-tweet-queue")
async def get_twitter_queue():
    redis_wrapper: RedisClientWrapper = app.state.redis_wrapper
    messages = await redis_wrapper.fifo_peek(TWEET_QUEUE)
    if not messages:
        return {"message": f"{TWEET_QUEUE} queue is empty."}
    return messages


@app.post("/clear-tweet-queue")
async def clear_tweet_queue(request: Request):
    redis_wrapper: RedisClientWrapper = request.app.state.redis_wrapper
    await redis_wrapper.fifo_clear(TWEET_QUEUE)
    return {"message": f"'{TWEET_QUEUE}' has been cleared."}


@app.get("/list-jobs")
async def list_scheduled_jobs(request: Request):
    """
    Lists the currently scheduled jobs and their next run times.
    """
    scheduler_wrapper: SchedulerWrapper = request.app.state.scheduler_wrapper
    jobs_info = scheduler_wrapper.get_jobs_info()
    return jobs_info
