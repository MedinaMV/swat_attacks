import subprocess
import requests
import concurrent.futures

# https://aicouncil.in
# http://testphp.vulnweb.com/

URL_SUBDOMAINS = f'/usr/src/app/tasks/files/subdomains.txt'
URL_XSS_PAYLOADS = f'/usr/src/app/tasks/files/xss_payload.txt'
URL_SQLI_PAYLOADS = f'/usr/src/app/tasks/files/sqli_payload.txt'

def generic_attack(subdomain: str, payloads: list):
    for payload in payloads:
        url_to_attack = subdomain[0:subdomain.find('=')+1]+ f'{payload}'
        r = requests.get(url_to_attack)
        if payload in r.text:
            return True, payload
            
def generic_task(subdomain, payloads):
    if subdomain[0:subdomain.find('=')+1].strip():
        vulnerable, reflection = generic_attack(subdomain, payloads)
        if vulnerable:
            return subdomain,reflection
        
def scanner(url_objetive,type):
    output_file = URL_SUBDOMAINS
    result = subprocess.run(['katana', '-u', url_objetive, '-o', output_file], capture_output=True, text=True)
    results = []

    if result.returncode == 0:
        subdomains = [line.rstrip() for line in open(URL_SUBDOMAINS,'r')]

        if type == 'xss':
            payloads_xss = [line.rstrip() for line in open(URL_XSS_PAYLOADS,'r')]
            results = execute(generic_task,payloads_xss,subdomains)
        
        if type == 'sqli':
            payloads_sqli = [line.rstrip() for line in open(URL_SQLI_PAYLOADS,'r')]
            results = execute(generic_task,payloads_sqli,subdomains)
    else:
        print(f"Error executing `katana`: {result.stderr}")
    return results

def execute(method, payloads, subdomains):
    scanner_result = []
    num_threads = 5

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = {executor.submit(method, subdomain, payloads): subdomain for subdomain in subdomains}

        for future in concurrent.futures.as_completed(futures):
            subdomain = futures[future]
            try:
                task = future.result()
                if task:
                    scanner_result.append(task)
            except Exception as e:
                print(f"An error occurred while processing {subdomain}: {e}")
    return scanner_result