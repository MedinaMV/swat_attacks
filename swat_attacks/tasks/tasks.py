from celery import shared_task
import time
from .models import task

@shared_task
def xss(queue='celery'):
    time.sleep(60)
    t = task(type='xss', done='2')
    t.save()
    return 'XSS done'

@shared_task
def sqli(queue='celery:1'):
    time.sleep(120)
    t = task(type='sqli', done='2')
    t.save()
    return 'SQLi done'
