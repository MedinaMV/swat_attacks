from celery import shared_task
import time

@shared_task
def xss(queue='celery'):
    time.sleep(60)
    return 'XSS done'

@shared_task
def sqli(queue='celery:1'):
    time.sleep(120)
    return 'SQLi done'
