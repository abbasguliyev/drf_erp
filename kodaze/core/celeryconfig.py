from __future__ import absolute_import

import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core', backend='redis://:ENA7eWv7s58AZCDm4MtyKVPe8oNd2690@redis:6379/0', broker='redis://:ENA7eWv7s58AZCDm4MtyKVPe8oNd2690@redis:6379/0')
app.conf.broker_url = 'redis://:ENA7eWv7s58AZCDm4MtyKVPe8oNd2690@redis:6379/0'

# app = Celery('core', backend='redis://127.0.0.1:6379/0', broker='redis://127.0.0.1:6379/0')
# app.conf.broker_url = 'redis://127.0.0.1:6379/0'

app.config_from_object('django.conf:settings')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "maas_goruntuleme_create_task": {
        "task": "maas_goruntuleme_create_task",
        "schedule": crontab(0,0,'*', day_of_month="1"),
    },
    "maas_goruntuleme_create_task_15": {
        "task": "maas_goruntuleme_create_task_15",
        "schedule": crontab(0,0,'*', day_of_month="15"),
    },
    "work_day_creater_task1": {
        "task": "work_day_creater_task1",
        "schedule": crontab(0, 0, '*', day_of_month="1"),
    },
    "work_day_creater_task15": {
        "task": "work_day_creater_task15",
        "schedule": crontab(0, 0, '*', day_of_month="15"),
    },

    "work_day_creater_holding_task1": {
        "task": "work_day_creater_holding_task1",
        "schedule": crontab(0, 0, '*', day_of_month="1"),
    },
    "work_day_creater_holding_task15": {
        "task": "work_day_creater_holding_task15",
        "schedule": crontab(0, 0, '*', day_of_month="15"),
    },

    "work_day_creater_shirket_task1": {
        "task": "work_day_creater_shirket_task1",
        "schedule": crontab(0, 0, '*', day_of_month="1"),
    },
    "work_day_creater_shirket_task15": {
        "task": "work_day_creater_shirket_task15",
        "schedule": crontab(0, 0, '*', day_of_month="15"),
    },

    "work_day_creater_ofis_task1": {
        "task": "work_day_creater_ofis_task1",
        "schedule": crontab(0, 0, '*', day_of_month="1"),
    },
    "work_day_creater_ofis_task15": {
        "task": "work_day_creater_ofis_task15",
        "schedule": crontab(0, 0, '*', day_of_month="15"),
    },

    "work_day_creater_shobe_task1": {
        "task": "work_day_creater_shobe_task1",
        "schedule": crontab(0, 0, '*', day_of_month="1"),
    },
    "work_day_creater_shobe_task15": {
        "task": "work_day_creater_shobe_task15",
        "schedule": crontab(0, 0, '*', day_of_month="15"),
    },

    "work_day_creater_komanda_task1": {
        "task": "work_day_creater_komanda_task1",
        "schedule": crontab(0, 0, '*', day_of_month="1"),
    },
    "work_day_creater_komanda_task15": {
        "task": "work_day_creater_komanda_task15",
        "schedule": crontab(0, 0, '*', day_of_month="15"),
    },

    "work_day_creater_vezife_task1": {
        "task": "work_day_creater_vezife_task1",
        "schedule": crontab(0, 0, '*', day_of_month="1"),
    },
    "work_day_creater_vezife_task15": {
        "task": "work_day_creater_vezife_task15",
        "schedule": crontab(0, 0, '*', day_of_month="15"),
    },
    "isci_fix_maas_auto_elave_et": {
        "task": "isci_fix_maas_auto_elave_et",
        "schedule": crontab(0, 0, '*', day_of_month="1"),
    },
    "demo": {
        "task": "demo",
        "schedule": crontab(0, 0, '*', day_of_month="1"),
    },
    "demo15": {
        "task": "demo",
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
}