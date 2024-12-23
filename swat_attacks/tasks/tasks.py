from celery import shared_task
from .attacks import scanner,bruteforce_type1,bruteforce_type2,nuclei_attacks,session_attacks
from .models import Generic_Result,Bruteforce_Result,Nuclei_Result,Session_Result
import json

def create_generic_result(data,level,attack_id,type):
    generic_result = Generic_Result()
    
    generic_result.attack_id = attack_id
    generic_result.results = [{'url': url, 'payload': payload} for url, payload in data]
    if type == 'xss':
        generic_result.info = 'Cross-Site Scripting (XSS)'
        generic_result.name = 'XSS'
        generic_result.level = 'M'
    else:
        generic_result.info = 'SQL Injection'
        generic_result.name = 'SQLI'
        generic_result.level = 'H'
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

def create_session_result(data,id):
    session_result = Session_Result()
    session_result.value_field = data['Value']
    session_result.expire_field = data['Expires']
    session_result.httponly_field = data['HttpOnly']
    session_result.hostonly_field = data['HostOnly']
    session_result.secure_field = data['Secure']
    session_result.samesite_field = data['SameSite']
    session_result.attack_id = id
    session_result.save()
    return

@shared_task
def generic_attack(data,id,type,queue='celery'):
    result = scanner(data['target'],type)
    create_generic_result(result,'H',id,type)
    return 

@shared_task
def bruteforce_attack(data,id,queue='celery:1'):
    body = json.loads(data['body'])
    ddos = bruteforce_type1(data['target'],data['endpoint'],data['method'],data['body'])
    result = bruteforce_type2(data['target'],data['endpoint'],data['method'],data['body'])
    create_bruteforce_result(ddos,body[next(iter(body))],result,'C',id)
    return 

@shared_task
def nuclei_attack(data,id,queue='celery:2'):
    result = nuclei_attacks(data['target'])
    create_nuclei_result(result,id)
    return

@shared_task
def session_attack(data,id,queue='celery:3'):
    result = session_attacks(data['target'],data['endpoint'],data['method'],data['body'])
    create_session_result(result,id)
    return
