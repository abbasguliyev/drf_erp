from __future__ import absolute_import

import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')


backend=os.environ['CELERY_RESULT_BACKEND']
broker=os.environ['CELERY_BROKER_URL']

app = Celery('core', backend=backend, broker=broker)
app.conf.broker_url = broker

# app = Celery('core', backend='redis://:ENA7eWv7s58AZCDm4MtyKVPe8oNd2690@redis:6379/0', broker='redis://:ENA7eWv7s58AZCDm4MtyKVPe8oNd2690@redis:6379/0')
# app.conf.broker_url = 'redis://:ENA7eWv7s58AZCDm4MtyKVPe8oNd2690@redis:6379/0'

# app = Celery('core', backend='redis://127.0.0.1:6379/0', broker='redis://127.0.0.1:6379/0')
# app.conf.broker_url = 'redis://127.0.0.1:6379/0'

app.config_from_object('django.conf:settings')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "salary_view_create_task_1": {
        "task": "salary_view_create_task",
        "schedule": crontab(0,0,'*', day_of_month="1"),
    },
    "salary_view_create_task_15": {
        "task": "salary_view_create_task",
        "schedule": crontab(0,0,'*', day_of_month="15"),
    },
    "employee_working_day_creater_task_1": {
        "task": "employee_working_day_creater_task",
        "schedule": crontab(0, 0, '*', day_of_month="1"),
    },
    "employee_working_day_creater_task_15": {
        "task": "employee_working_day_creater_task",
        "schedule": crontab(0, 0, '*', day_of_month="15"),
    },

    "employee_fix_prim_auto_add": {
        "task": "employee_fix_prim_auto_add",
        "schedule": crontab(0, 0, '*', day_of_month="1"),
    },
    "demo_create_task_1": {
        "task": "demo_create_task",
        "schedule": crontab(0, 0, '*', day_of_month="1"),
    },
    "demo_create_task_15": {
        "task": "demo_create_task",
        "schedule": crontab(0, 0, '*', day_of_month="15"),
    },
    "backup": {
        "task": "backup",
        "schedule": crontab(0, 0, '*', day_of_month="1"),
    },
    "mediabackup": {
        "task": "mediabackup",
        "schedule": crontab(0, 0, '*', day_of_month="1"),
    },
    "manage_task_manager": {
        "task": "manage_task_manager",
        "schedule": crontab(hour="2", minute="0"),
    },
    "task_that_reduce_guarantee_of_service_every_day": {
        "task": "task_that_reduce_guarantee_of_service_every_day",
        "schedule": crontab(hour=0, minute=0),
    },
}