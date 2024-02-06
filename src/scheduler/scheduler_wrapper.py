import logging
import random
import scheduler.jobs as jobs
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.base import JobLookupError

DAILY_NUMBER_OF_TWEET_GENERATIONS = 5
DAILY_NUMBER_OF_IMAGE_GENERATIONS = 5
DAILY_NUMBER_OF_TEXT_TWEETS = 10
DAILY_NUMBER_OF_IMAGE_TWEETS = 2


class SchedulerWrapper:
    def __init__(self, redis_wrapper, start: bool = True):
        self.scheduler = AsyncIOScheduler()
        self.redis_wrapper = redis_wrapper
        self.initialize_scheduler(start)

    def initialize_scheduler(self, start: bool) -> None:
        # Add the periodic reshuffle job
        job_id = "periodic_scheduler_job_time_reshuffle"
        hour, minute = 0, 0

        self.scheduler.add_job(
            self.periodic_scheduler_job_time_reshuffle,
            trigger='cron',
            hour=hour,
            minute=minute,
            id=job_id
        )
        logging.info(
            f"`{job_id}` will run today at: {hour:02d}:{minute:02d}")

        # Add other jobs to the scheduler
        self.add_jobs_to_scheduler()
        if start:
            self.scheduler.start()

    def calculate_run_times(self, num_runs: int) -> list:
        interval = 24 // num_runs
        return [f"{i * interval:02d}:00" for i in range(num_runs)]

    def add_jobs_to_scheduler(self):
        # Add tweet generation jobs
        times_to_run = self.calculate_run_times(
            DAILY_NUMBER_OF_TWEET_GENERATIONS)
        for i, time in enumerate(times_to_run):
            job_id = f"generate_tweets_job_{i+1}"
            hour, minute = map(int, time.split(':'))

            self.scheduler.add_job(
                jobs.generate_tweets_job,
                trigger='cron',
                hour=hour,
                minute=minute,
                id=job_id,
                args=[self.redis_wrapper]
            )

            logging.info(
                f"`{job_id}` will run today at: {hour:02d}:{minute:02d}")

        # Add text tweet posting jobs
        for i in range(DAILY_NUMBER_OF_TEXT_TWEETS):
            job_id = f"post_text_tweet_job_{i+1}"
            hour, minute = random.randint(0, 23), random.randint(0, 59)

            self.scheduler.add_job(
                jobs.post_text_tweet_job,
                trigger='cron',
                hour=hour,
                minute=minute,
                id=job_id,
                args=[self.redis_wrapper]
            )

            logging.info(
                f"`{job_id}` will run today at: {hour:02d}:{minute:02d}")

        # # Add image tweet posting jobs
        # for i in range(DAILY_NUMBER_OF_IMAGE_TWEETS):
        #     hour, minute = random.randint(0, 23), random.randint(0, 59)
        #     job_id = f"post_image_tweet_job_{i+1}"
        #     self.scheduler.add_job(
        #         jobs.post_image_tweet_job, 'cron', hour=hour, minute=minute, id=job_id)
        #     logging.info(
        #         f"`{job_id}` will run today at {hour:02d}:{minute:02d}")

    async def periodic_scheduler_job_time_reshuffle(self):
        for job in self.scheduler.get_jobs():
            try:
                if not job.id.startswith("periodic"):
                    self.scheduler.remove_job(job.id)
            except JobLookupError:
                pass  # Job was already removed or does not exist
        self.add_jobs_to_scheduler()
