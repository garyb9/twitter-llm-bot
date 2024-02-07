import json
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

    def calculate_run_times_random(self, num_runs: int) -> list:
        return [
            f"{random.randint(0, 23):02d}:{random.randint(0, 59)}"
            for _ in range(num_runs)
        ]

    def add_jobs_to_scheduler(self) -> None:
        # Add tweet generation jobs
        times_to_run = self.calculate_run_times(
            DAILY_NUMBER_OF_TWEET_GENERATIONS)
        self.add_jobs(jobs.generate_tweets_job,
                      "generate_tweets_job", times_to_run)

        # Add text tweet posting jobs
        times_to_run = self.calculate_run_times_random(
            DAILY_NUMBER_OF_TEXT_TWEETS)
        self.add_jobs(jobs.post_text_tweet_job,
                      "post_text_tweet_job", times_to_run)

    def add_jobs(self, job_function, job_id_base, times_to_run) -> None:
        for i, time in enumerate(times_to_run):
            hour, minute = map(int, time.split(':'))
            job_id = f"{job_id_base}_{i+1}"

            self.scheduler.add_job(
                job_function,
                trigger='cron',
                hour=hour,
                minute=minute,
                id=job_id,
                args=[self.redis_wrapper]
            )

        logging.info(
            f"{job_id_base} will run at: \n{json.dumps(times_to_run, indent=2)}")

    async def periodic_scheduler_job_time_reshuffle(self) -> None:
        for job in self.scheduler.get_jobs():
            try:
                if not job.id.startswith("periodic"):
                    self.scheduler.remove_job(job.id)
            except JobLookupError:
                pass  # Job was already removed or does not exist
        self.add_jobs_to_scheduler()
