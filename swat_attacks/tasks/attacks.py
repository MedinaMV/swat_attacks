import subprocess
import requests
import concurrent.futures
from http.cookies import SimpleCookie
import re
import json

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

def bruteforce_type1(url,endpoint,method,data):
    body = json.loads(data)
    cont = 0
    for i in range(0,10):
        try:
            if method == 'POST':
                requests.post(url+endpoint, data=body)
            else:
                requests.put(url+endpoint, data=body)
            cont = i
        except requests.exceptions.HTTPError as err:
            print(f'HTTP error occurred: {err}')
    return cont > 5

def bruteforce_type2(url,endpoint,method,data):
    body = json.loads(data)
    result = ''
    base_page = ''
    keys = list(body.keys())
    first_key = keys[0]
    second_key = keys[1]
    passwords = [line.rstrip() for line in open(URL_PASSWORDS,'r')]
    if method == 'POST':
        base_page = requests.post(url+endpoint, data={first_key:body[first_key],second_key:"password"}).content
    else:
        base_page = requests.put(url+endpoint, data={first_key:body[first_key],second_key:"password"}).content
    for password in passwords:
        body_with_password = {first_key:body[first_key],second_key:password}
        print(body_with_password)
        try:
            if method == 'POST':
                response = requests.post(url+endpoint, data=body_with_password)
            else:
                response = requests.put(url+endpoint, data=body_with_password)
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

def session_attacks(url,endpoint,method,data):
    body = json.loads(data)
    if method == 'POST':
        response = requests.post(url+endpoint, data=body)
    else:
        response = requests.put(url+endpoint, data=body)
    cookies = obtain_cookies(response)
    result = {}
    for cookie in response.cookies:
        result['Name'] = cookie.name 
        result['Value'] = secure_value(cookie.name)
        result['Expires'] = cookie.expires != None
        result['HttpOnly'] = has_http_only(cookie)
        result['Secure'] = cookie.secure
        result['SameSite'] = cookie.get_nonstandard_attr('SameSite') != None

    for cookie in cookies:
        result['HostOnly'] = cookie['hostonly']
    return result

def obtain_cookies(response):
    cookie_header = response.headers.get('Set-Cookie')
    if not cookie_header:
        return []

    simple_cookie = SimpleCookie()
    simple_cookie.load(cookie_header)

    cookies = []
    for key, morsel in simple_cookie.items():
        cookie = {
            'domain': morsel['domain']
        }
        cookie['hostonly'] = not bool(cookie['domain'])
        cookies.append(cookie)
    return cookies
    
def secure_value(valor):
    if len(valor) <= 20:
        return False

    if not re.match(r'^[A-Za-z0-9\.\-_]+$', valor):
        return False

    if '%' in valor or '/' in valor:
        return False

    return True

def has_http_only(cookie):
    extra_args = cookie.__dict__.get('_rest')
    if extra_args:
        for key in extra_args.keys():
            if key.lower() == 'httponly':
                return True
    return False