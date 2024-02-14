import json
import logging
import random
import consts
from typing import List
from datetime import datetime, timedelta
from db.redis_wrapper import RedisClientWrapper
import scheduler.jobs as jobs
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.base import JobLookupError


class SchedulerWrapper:
    def __init__(self, redis_wrapper: RedisClientWrapper):
        self.scheduler = AsyncIOScheduler()
        self.redis_wrapper = redis_wrapper
        self.initialize_scheduler()

    def initialize_scheduler(self) -> None:
        logging.info("Initializing scheduler...")

        # Add the periodic jobs first
        self.scheduler.add_job(
            self.periodic_job_time_reshuffle,
            trigger='cron',
            hour=0,
            minute=0,
            id="periodic_job_time_reshuffle",
        )

        self.scheduler.add_job(
            self.periodic_job_time_print,
            trigger='interval',
            minutes=30,
            id="periodic_job_time_print",
        )

        # Add all other jobs to the scheduler and start
        self.init_sheduler_jobs()
        self.scheduler.start()

        # Add jobs to run immediately
        run_time = datetime.now(self.scheduler.timezone) + \
            timedelta(minutes=1)  # run in a minute from now
        formatted_run_time = run_time.strftime("%H:%M")

        self.add_job_to_scheduler(
            jobs.generate_tweets_job,
            "generate_tweets_job_init",
            [formatted_run_time],
            self.redis_wrapper
        )

        # Log times
        run_times = json.dumps(self.get_jobs_info(), indent=4)
        logging.info(f"Scheduler => Jobs running: {run_times}")

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
            consts.DAILY_NUMBER_OF_TWEET_GENERATIONS)
        self.add_job_to_scheduler(
            jobs.generate_tweets_job,
            "generate_tweets_job",
            times_to_run,
            self.redis_wrapper
        )

        # Add text tweet posting jobs
        times_to_run = self.calculate_run_times_random(
            consts.DAILY_NUMBER_OF_TEXT_TWEETS)
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

        # logging.info(
        #     f"{job_id_base} will run at: \n{json.dumps(times_to_run, indent=2)}")

    def get_jobs_info(self) -> List[str]:
        """
        Retrieves information about currently scheduled jobs.
        """
        jobs_info = []
        now = datetime.now(self.scheduler.timezone)
        for job in self.scheduler.get_jobs():
            run_time = job.next_run_time.strftime(
                "%H:%M") if job.next_run_time else "None"
            time_until = (job.next_run_time -
                          now).total_seconds() if job.next_run_time else 0
            minutes_until = time_until // 60
            seconds_until = time_until % 60
            jobs_info.append(
                f"{job.id} -> {run_time} ({int(minutes_until)}m {int(seconds_until)}s)"
            )
        return jobs_info

    async def periodic_job_time_reshuffle(self) -> None:
        for job in self.scheduler.get_jobs():
            try:
                if not job.id.startswith("periodic"):
                    self.scheduler.remove_job(job.id)
            except JobLookupError:
                pass  # Job was already removed or does not exist
        self.init_sheduler_jobs()
        run_times = json.dumps(self.get_jobs_info(), indent=4)
        logging.info(f"Scheduler => Jobs running: {run_times}")

    async def periodic_job_time_print(self) -> None:
        run_times = json.dumps(self.get_jobs_info()[0:5], indent=4)
        logging.info(f"Scheduler => Next jobs: {run_times}")
