import subprocess
import requests
import concurrent.futures

# https://aicouncil.in
# http://testphp.vulnweb.com/

URL_SUBDOMAINS = f'/usr/src/app/tasks/files/subdomains.txt'
URL_XSS_PAYLOADS = f'/usr/src/app/tasks/files/xss_payload.txt'
URL_SQLI_PAYLOADS = f'/usr/src/app/tasks/files/sqli_payload.txt'
URL_PASSWORDS = f'/usr/src/app/tasks/files/rock.txt'
URL_NUCLEI = f'/usr/src/app/tasks/files/nuclei_results.txt'

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

def scanner(url_objetive,type):
    result = subprocess.run(['katana', '-u', url_objetive, '-o', URL_SUBDOMAINS], capture_output=True, text=True)
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

def bruteforce_type1(url,username_type,password_type):
    cont = 0
    data = {username_type:'admin',password_type:'password'}
    for i in range(0,10):
        try:
            requests.post(url, data=data)
            cont = i
        except requests.exceptions.HTTPError as err:
            print(f'HTTP error occurred: {err}')
            
    return cont > 5

def bruteforce_type2(url,username,username_type,password_type):
    result = ''
    passwords = [line.rstrip() for line in open(URL_PASSWORDS,'r')]
    base_page = requests.get(url).content
    for password in passwords:
        try:
            data = {username_type:username,password_type:password}
            response = requests.post(url, data=data)
            if base_page != response.content:
                result = password
                break
        except requests.exceptions.HTTPError as err:
            print(f'HTTP error ocurred: {err}')
    return result

def nuclei_attacks(url):
    result = subprocess.run(['nuclei', '-u', url, '-o', URL_NUCLEI], capture_output=True, text=True)
    nuclei_results = []

    if result.returncode == 0:
        vulnerabilities = [line.rstrip() for line in open(URL_NUCLEI,'r')]
        filter_lines = [line for line in vulnerabilities if not line.startswith('[INF]')]
        nuclei = [line.replace('[', '').replace(']', '') for line in filter_lines]
        nuclei_results = [{'vulnerability': element} for element in nuclei]

    else:
        print(f"Error executing `nuclei`: {result.stderr}")

    return nuclei_results