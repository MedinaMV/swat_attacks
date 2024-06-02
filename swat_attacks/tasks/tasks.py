from celery import shared_task
import time
from .attacks import xss_scanner
from .models import Generic_Result
from datetime import datetime
import pytz

def create_generic_result(data,level,attack_id):
    ur, pay = zip(*data)
    payloads = list(pay)
    urls = list(ur)
    clean_payloads = [payload.replace("'", "") for payload in payloads]
    clean_urls = [url.replace("'", "") for url in urls]
    #print(clean_payloads)
    #print(clean_urls)
    result_data = {
        "vulnerable_urls": clean_urls,
        "payloads": clean_payloads,
        "level": level,
        "attack_id": attack_id,
        "created_at": datetime.now(pytz.timezone('UTC')).isoformat()
    }
    return result_data

@shared_task
def xss(data,id,queue='celery'):
    result = xss_scanner(data['target'],id)
    generic_result = Generic_Result(create_generic_result(result,'HIGH',id))
    print(type(generic_result['vulnerable_urls']))
    generic_result.save()
    return 

@shared_task
def sqli(url,id,queue='celery:1'):
    time.sleep(5)
    print('SQLI ATTACK COMPLETED')
    return

    

    