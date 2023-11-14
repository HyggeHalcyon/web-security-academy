# Lab: Information disclosure in error messages
# difficulty: apprentice

import requests

sub = '0a02007603968a07827c7e3f006f0000'
url = f'https://{sub}.web-security-academy.net'

def main():
    endpoint = '/product?productId=ERROR'
    r = requests.get(url + endpoint)
    print(r.text.split('\n')[-1])

if __name__ == '__main__':
    main()