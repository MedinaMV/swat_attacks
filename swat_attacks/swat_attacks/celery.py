import os 
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'swat_attacks.settings')

app = Celery('swat_attacks',backend='redis://redis:6379/0')
app.config_from_object("django.conf:settings", namespace="CELERY")
# app.conf.task_routes = {'tasks.tasks.task1': {'queue':'queue1'}, 'tasks.tasks.task2': {'queue':'queue2'}}

app.conf.broker_transport_options = {
    'priority_steps': list(range(10)),
    'sep':':',
    'queue_order_strategy':'priority',
}


app.autodiscover_tasks()