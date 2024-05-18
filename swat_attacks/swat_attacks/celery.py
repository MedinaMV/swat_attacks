import os 
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'swat_attacks.settings')

app = Celery('swat_attacks')
app.config_from_object("django.conf:settings", namespace="CELERY")

@app.task
def test():
    return 'Testing'

app.autodiscover_tasks()