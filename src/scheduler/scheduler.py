import random
import scheduler.jobs as jobs
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.base import JobLookupError

DAILY_NUMBER_OF_TEXT_TWEETS = 12
DAILY_NUMBER_OF_IMAGE_TWEETS = 2


def create_scheduler(start: bool = True):
    scheduler = AsyncIOScheduler()
    # separating the periodic reshuffle to be added only once
    scheduler.add_job(
        periodic_scheduler_job_time_reshuffle,
        'cron',
        hour=0,
        minute=0,
        id=f"periodic_scheduler_job_time_reshuffle"
    )
    # add other jobs to the scheduler
    add_jobs_to_scheduler(scheduler)
    if start:
        scheduler.start()
    return scheduler


def add_jobs_to_scheduler(scheduler: AsyncIOScheduler):
    for i in range(DAILY_NUMBER_OF_TEXT_TWEETS):
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        scheduler.add_job(jobs.post_text_tweet_job, 'cron', hour=hour,
                          minute=minute, id=f"post_text_tweet_job_{i}")
    for i in range(DAILY_NUMBER_OF_IMAGE_TWEETS):
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        scheduler.add_job(jobs.post_image_tweet_job, 'cron', hour=hour,
                          minute=minute, id=f"post_image_tweet_job_{i}")


async def periodic_scheduler_job_time_reshuffle(scheduler: AsyncIOScheduler):
    # Clear existing jobs to avoid duplication
    for job in scheduler.get_jobs():
        try:
            if not job.id.startswith("periodic"):
                scheduler.remove_job(job.id)
        except JobLookupError:
            pass  # Job was already removed or does not exist
    add_jobs_to_scheduler(scheduler)
