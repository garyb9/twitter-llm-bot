import json
import logging
import random
from typing import List
from datetime import datetime, timedelta
from db.redis_wrapper import RedisClientWrapper
import scheduler.jobs as jobs
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.base import JobLookupError

DAILY_NUMBER_OF_TWEET_GENERATIONS = 2
DAILY_NUMBER_OF_IMAGE_GENERATIONS = 5
DAILY_NUMBER_OF_TEXT_TWEETS = 25
DAILY_NUMBER_OF_IMAGE_TWEETS = 2


class SchedulerWrapper:
    def __init__(self, redis_wrapper: RedisClientWrapper):
        logging.info("Starting scheduler...")
        self.scheduler = AsyncIOScheduler()
        self.redis_wrapper = redis_wrapper
        self.initialize_scheduler()
        logging.info("Scheduler running.")

    def initialize_scheduler(self) -> None:
        # Add the periodic reshuffle job first

        self.add_job_to_scheduler(
            self.periodic_scheduler_job_time_reshuffle,
            "periodic_scheduler_job_time_reshuffle",
            ["00:00"]
        )

        # Add all other jobs to the scheduler and start
        self.init_sheduler_jobs()
        self.scheduler.start()

        # Add jobs to run immediately
        run_time = datetime.now() + timedelta(minutes=1)  # run in a minute from now
        formatted_run_time = run_time.strftime("%H:%M")

        self.add_job_to_scheduler(
            jobs.generate_tweets_job,
            "generate_tweets_job_init",
            [formatted_run_time],
            self.redis_wrapper
        )

    def calculate_run_times(self, num_runs: int) -> list:
        interval = 24 // num_runs
        return [f"{i * interval:02d}:00" for i in range(num_runs)]

    def calculate_run_times_random(self, num_runs: int) -> list:
        return [
            f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}"
            for _ in range(num_runs)
        ]

    def init_sheduler_jobs(self) -> None:
        # Add tweet generation jobs
        times_to_run = self.calculate_run_times(
            DAILY_NUMBER_OF_TWEET_GENERATIONS)
        self.add_job_to_scheduler(
            jobs.generate_tweets_job,
            "generate_tweets_job",
            times_to_run,
            self.redis_wrapper
        )

        # Add text tweet posting jobs
        times_to_run = self.calculate_run_times_random(
            DAILY_NUMBER_OF_TEXT_TWEETS)
        times_to_run.sort()
        self.add_job_to_scheduler(
            jobs.post_text_tweet_job,
            "post_text_tweet_job",
            times_to_run,
            self.redis_wrapper
        )

        # TODO: add image generation jobs

    def add_job_to_scheduler(self, job_function, job_id_base: str, times_to_run: List[str], *args) -> None:
        for i, time in enumerate(times_to_run):
            hour, minute = map(int, time.split(':'))
            job_id = f"{job_id_base}_{i+1}"

            self.scheduler.add_job(
                job_function,
                trigger='cron',
                hour=hour,
                minute=minute,
                id=job_id,
                args=args
            )

        logging.info(
            f"{job_id_base} will run at: \n{json.dumps(times_to_run, indent=2)}")

    def get_jobs_info(self) -> List[str]:
        """
        Retrieves information about currently scheduled jobs.
        """
        jobs_info = []
        for job in self.scheduler.get_jobs():
            run_time = job.next_run_time.strftime(
                "%H:%M") if job.next_run_time else "None"
            jobs_info.append(f"{job.id} -> {run_time}")
        return jobs_info

    async def periodic_scheduler_job_time_reshuffle(self) -> None:
        for job in self.scheduler.get_jobs():
            try:
                if not job.id.startswith("periodic"):
                    self.scheduler.remove_job(job.id)
            except JobLookupError:
                pass  # Job was already removed or does not exist
        self.init_sheduler_jobs()
