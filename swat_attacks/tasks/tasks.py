from celery import shared_task
from .attacks import scanner, bruteforce_type1, bruteforce_type2
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
    create_generic_result(result,'HIGH',id)
    return 

@shared_task
def bruteforce_attack_1(data):
    bruteforce_type1()
    return 

@shared_task
def bruteforce_attack_2(data):
    bruteforce_type2()
    return 