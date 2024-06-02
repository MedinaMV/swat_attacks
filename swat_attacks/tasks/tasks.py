from celery import shared_task
import time
import pytz
from datetime import datetime
from .attacks import xss_scanner
from .models import Generic_Result

def create_generic_result(data,level,attack_id):
    generic_result = Generic_Result()
    generic_result.level = level
    generic_result.attack_id = attack_id
    generic_result.results = [{'url': url, 'payload': payload} for url, payload in data]
    generic_result.save()
    return generic_result

@shared_task
def xss(data,id,queue='celery'):
    result = xss_scanner(data['target'],id)
    create_generic_result(result,'HIGH',id)
    return 

@shared_task
def sqli(url,id,queue='celery:1'):
    time.sleep(5)
    print('SQLI ATTACK COMPLETED')
    return