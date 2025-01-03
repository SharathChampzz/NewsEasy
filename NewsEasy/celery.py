# NewsEasy/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NewsEasy.settings")

app = Celery("NewsEasy")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


app.conf.beat_schedule = {
    "scrape-every-hour": {
        "task": "NewsEasy.scrapper.main.save_news_to_db",
        "schedule": crontab(
            minute=0, hour="*/1"
        ),  # Every hour (e.g. 1:00, 2:00, 3:00, etc.)
        # 'schedule': crontab(minute='*/50'), # Every 5 minutes past the hour (e.g. 12:05, 12:10, 12:15, etc.)
        # 'schedule': crontab(minute=30, hour='*'), # Every 30 minute past the hour (e.g. 12:30, 1:30, 2:30, etc.)
        # 'schedule': crontab(hour=8, minute=0), # Every day at 8:00 AM (e.g. 8:00, 8:00, 8:00, etc.)
        # 'schedule': crontab(day_of_week='mon,tue,wed,thu,fri'), # Every weekday (Monday to Friday)
        # 'schedule': crontab(day_of_month=15), # Every 15th of the month (e.g. 15th of January, 15th of February, etc.)
    },
}
