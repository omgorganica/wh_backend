#  celery -A backend worker -l info -P gevent
#  celery -A backend beat

import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'badges.settings')

app = Celery('badges')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'null_balance': {
        'task': 'backend.tasks.null_balance',
        'schedule': crontab(minute='*/1'),  #crontab(0, 0,month_of_year='*/3') Первый день каждого квартала
    },
}

#