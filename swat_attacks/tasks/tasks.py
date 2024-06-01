from celery import shared_task
import time
from .attacks import xss_scanner

@shared_task
def xss(data, id, queue='celery'):
    result = xss_scanner(data['target'],id)
    print(result)
    return 

@shared_task
def sqli(url, id, queue='celery:1'):
    time.sleep(120)
    print('SQLI ATTACK COMPLETED')
    return

    

    