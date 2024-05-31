import subprocess
import requests
import concurrent.futures

# https://aicouncil.in
# http://testphp.vulnweb.com/

def xss_attack(subdomain: str, payloads: list):
    for payload in payloads:
        url_to_attack = subdomain[0:subdomain.find('=')+1]+ f'{payload}'
        r = requests.get(url_to_attack)
        if payload in r.text:
            return True, payload
            
def xss_task(subdomain, payloads):
    if subdomain[0:subdomain.find('=')+1].strip():
        vulnerable, reflection = xss_attack(subdomain, payloads)
        if vulnerable:
            return subdomain,reflection

def xss_scanner(url_objetive):

    output_file = '/usr/src/app/tasks/files/subdomains.txt'

    result = subprocess.run(['katana', '-u', url_objetive, '-o', output_file], capture_output=True, text=True)

    if result.returncode == 0:
        subdomains = [line.rstrip() for line in open('/usr/src/app/tasks/files/subdomains.txt','r')]
        #payloads = [line.rstrip() for line in open('/usr/src/app/tasks/files/xss-payload-list.txt','r')]
        payloads = [line.rstrip() for line in open('/usr/src/app/tasks/files/xss_payload.txt','r')]

        num_threads = 5

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = {executor.submit(xss_task, subdomain, payloads): subdomain for subdomain in subdomains}

            for future in concurrent.futures.as_completed(futures):
                subdomain = futures[future]
                try:
                    print(future.result())
                except Exception as e:
                    print(f"An error occurred while processing {subdomain}: {e}")
    else:
        print(f"Error al ejecutar `katana`: {result.stderr}")