from apscheduler.schedulers.background import BackgroundScheduler
import twitter_jobs

# Create a scheduler instance
scheduler = BackgroundScheduler(daemon=True)

# Add CRON tasks
scheduler.add_job(twitter_jobs.get_tweets_job, 'cron', hour=12, minute=0, second=0) # Runs daily at 12:00 PM
scheduler.add_job(twitter_jobs.post_tweet_job, 'interval', minutes=30) # Runs every 30 minutes

# # Define the times at which the task should run (midnight, 8 AM, 12 PM, 4 PM, 8 PM)
# times_to_run = ['0 0', '0 8', '0 12', '0 16', '0 20']

# # Add jobs for each specific time
# for time in times_to_run:
#     hour, minute = time.split()
#     scheduler.add_job(twitter_jobs.create_tweet_job, 'cron', hour=hour, minute=minute)

# Debug
# scheduler.add_job(lambda: print("Sample task executed!"), 'interval', seconds=10) # Runs every 10 seconds