from celery import shared_task
import time
from .attacks import xss_scanner

@shared_task
def xss(data, queue='celery'):
    xss_scanner(data['target'])
    return 

@shared_task
def sqli(queue='celery:1'):
    time.sleep(120)
    print('SQLI ATTACK COMPLETED')
    return

    

    