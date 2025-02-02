import os
from celery import Celery
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


app = Celery('tasks', broker=os.getenv('REDIS_URL'))

@app.task
def run_spider():
    process = CrawlerProcess(get_project_settings())
    process.crawl('tefl_jobs')
    process.start()

app.conf.beat_schedule = {
    'run-spider-hourly': {
        'task': 'tasks.run_spider',
        'schedule': 3600.0,  # Every hour
    },
}