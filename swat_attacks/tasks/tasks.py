from celery import shared_task
from .attacks import scanner,bruteforce_type1,bruteforce_type2,nuclei_attacks
from .models import Generic_Result,Bruteforce_Result,Nuclei_Result

def create_generic_result(data,level,attack_id):
    generic_result = Generic_Result()
    generic_result.level = level
    generic_result.attack_id = attack_id
    generic_result.results = [{'url': url, 'payload': payload} for url, payload in data]
    generic_result.save()
    return generic_result

def create_bruteforce_result(ddos,username,result,level,attack_id):
    bruteforce_result = Bruteforce_Result()
    bruteforce_result.vulnerable_ddos = ddos
    bruteforce_result.username = username
    bruteforce_result.password = result
    bruteforce_result.level = level
    bruteforce_result.attack_id = attack_id
    bruteforce_result.save()
    return 

def create_nuclei_result(data,id):
    nuclei_result = Nuclei_Result()
    nuclei_result.results = data
    nuclei_result.attack_id = id
    nuclei_result.save()
    return

@shared_task
def generic_attack(data,id,type,queue='celery'):
    result = scanner(data['target'],type)
    create_generic_result(result,'HIGH',id)
    return 

@shared_task
def bruteforce_attack(data,id,queue='celery:1'):
    ddos = bruteforce_type1(data['bruteforce']['url'],data['bruteforce']['username_type'],data['bruteforce']['password_type'])
    result = bruteforce_type2(data['bruteforce']['url'],data['bruteforce']['username'],data['bruteforce']['username_type'],data['bruteforce']['password_type'])
    create_bruteforce_result(ddos,data['bruteforce']['username'],result,'MEDIUM',id)
    return 

@shared_task
def nuclei_attack(data,id,queue='celery:2'):
    result = nuclei_attacks(data['target'])
    create_nuclei_result(result,id)
    return
