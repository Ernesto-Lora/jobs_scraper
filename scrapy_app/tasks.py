import os
from celery import Celery
import subprocess

app = Celery('tasks', broker=os.getenv('REDIS_URL'), backend=os.getenv('REDIS_URL'))

@app.task
def run_spider():
    # Run the spider using the `scrapy crawl` command
    subprocess.run(["scrapy", "crawl", "tefl_jobs"])

app.conf.beat_schedule = {
    'run-spider-hourly': {
        'task': 'tasks.run_spider',
        'schedule': 30.0,  # Every hour
    },
}