from celery import shared_task
from .attacks import scanner,bruteforce_type1,bruteforce_type2,nuclei_attacks,session_attacks
from .models import Generic_Result,Bruteforce_Result,Nuclei_Result,Session_Result

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
    print(data)
    '''result = scanner(data['target'],type)
    create_generic_result(result,'H',id)'''
    return 

@shared_task
def bruteforce_attack(data,id,queue='celery:1'):
    print(data)
    '''ddos = bruteforce_type1(data['bruteforce']['url'],data['bruteforce']['username_type'],data['bruteforce']['password_type'])
    result = bruteforce_type2(data['bruteforce']['url'],data['bruteforce']['username'],data['bruteforce']['username_type'],data['bruteforce']['password_type'])
    create_bruteforce_result(ddos,data['bruteforce']['username'],result,'M',id)'''
    return 

@shared_task
def nuclei_attack(data,id,queue='celery:2'):
    print(data)
    '''result = nuclei_attacks(data['target'])
    create_nuclei_result(result,id)'''
    return

@shared_task
def session_attack(data,id,queue='celery:3'):
    print(data)
    '''result = session_attacks(data['session']['url'],data['session']['username'],data['session']['password'],data['session']['username_type'],data['session']['password_type'])
    create_session_result(result,id)'''
    return
