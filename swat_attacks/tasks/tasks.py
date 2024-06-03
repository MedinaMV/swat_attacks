from celery import shared_task
from .attacks import scanner
from .models import Generic_Result

def create_generic_result(data,level,attack_id):
    generic_result = Generic_Result()
    generic_result.level = level
    generic_result.attack_id = attack_id
    generic_result.results = [{'url': url, 'payload': payload} for url, payload in data]
    generic_result.save()
    return generic_result

@shared_task
def generic_attack(data,id,type,queue='celery'):
    result = scanner(data['target'],type)
    #print(result)
    create_generic_result(result,'HIGH',id)
    return 