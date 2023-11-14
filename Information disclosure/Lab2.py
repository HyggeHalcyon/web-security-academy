# Lab: Information disclosure on debug page
# difficulty: apprentice

import requests

sub = '0a89004303b28633818102da0023001b'
url = f'https://{sub}.web-security-academy.net'

def main():
    endpoint = '/cgi-bin/phpinfo.php'
    r = requests.get(url + endpoint)
    print(r.text.split('\n')[598])

if __name__ == '__main__':
    main()