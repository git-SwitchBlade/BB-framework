import requests
import json
import sys
import asyncio
import aiohttp

class color:
    blue = '\033[94m'
    green = '\033[92m'
    red = '\033[93m'
    underline = '\033[4m'
    reset = '\033[0m'

subdomains = set()
search = sys.argv[1]
base_url = f"https://crt.sh/?q={search}&output=json"


def getData(base_url):

    response = requests.get(base_url)
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        x = json.loads(content)
        for i in range(len(x)):
            name_value = x[i]['name_value']
            if name_value.find('\n'):
                subname_value = name_value.split('\n')
                for subname_value in subname_value:
                    if subname_value.find('*'):
                        if subname_value not in subdomains:
                            subdomains.add(subname_value)
        return subdomains
    elif response.status_code == 404:
        print(f'{color.red}No Sub-Domains Found For This Domain{color.reset}')


async def checkDomain(subdomains):
    async with aiohttp.ClientSession() as session:
        for domain in subdomains:
            url = f"https://{domain}"
            try:
                async with session.get(url , ssl = False) as checkAlive:
                    if checkAlive.status == 200:
                        print(f"{color.green}200 ok {url}{color.reset}")
                    elif checkAlive.status == 404:
                        print(f"404 Not Found {url}")
                    else:
                        print("Some error ocurred")
            except aiohttp.ClientConnectorError:
                print(f"{color.red}Connection refused but status code 200 by {url}{color.reset}")



if __name__ == '__main__':
    print(f"{color.green}[+] Checking For Sub-Domains in{color.reset} {search}")
    print(f"{color.green}----------------------------------------------------------{color.reset}")
    getData(base_url)
    for data in subdomains:
        print(f"{color.blue}{data}{color.reset}")
    print("\n\n")
    print(f"{color.blue} Check For Active Sub-Domains{color.reset}")
    asyncio.run(checkDomain(subdomains))
        
    

    