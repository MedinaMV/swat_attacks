from celery import shared_task
import time

@shared_task
def xss(queue='celery'):
    time.sleep(60)
    print('XSS ATTACK COMPLETED')
    return 

@shared_task
def sqli(queue='celery:1'):
    time.sleep(120)
    print('SQLI ATTACK COMPLETED')
    return
