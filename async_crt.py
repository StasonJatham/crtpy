
import aiohttp
import asyncio
import aiodns
import aiofiles as aiof
import requests
import json
from urllib.parse import urlparse
import requests, json

class crtshAPI(object):
    def search(self, domain, wildcard=True, expired=True):
        base_url = "https://crt.sh/?q={}&output=json"
        if not expired:
            base_url = base_url + "&exclude=expired"
        if wildcard and "%" not in domain:
            domain = "%.{}".format(domain)
        url = base_url.format(domain)

        ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
        req = requests.get(url, headers={'User-Agent': ua})

        if req.ok:
            try:
                content = req.content.decode('utf-8')
                data = json.loads(content)
                return data
            except ValueError:
                data = json.loads("[{}]".format(content.replace('}{', '},{')))
                return data
            except Exception as err:
                print("Error retrieving information.")
        return None
    

                
                
async def query(resolver, name, query_type):
    try:
        res = await resolver.query(name, query_type)
    except Exception as e:
        return (name,None)
    return (name,res[0].host)

async def log_output(filename, text):
    async with aiof.open(filename, "w") as out:
        await out.write(text)
        await out.flush()


async def fetch(session, url):
    try:
        async with session.head(url,timeout=2) as response:
            return (url, response.status)
    except Exception:
        try:
            async with session.get(url,timeout=2) as response:
                return (url, response.status)
        except Exception:
            return (url,None) 
    


def get_urls(start):
    site_infos = crtshAPI().search(start)

    url_list = []
    for info in site_infos:
        dom = info.get('common_name').replace("*.","") 
        if dom not in url_list:
            url_list.append(info.get('common_name'))
            
        if info.get('name_value'):
            sub = info.get('name_value').replace("*.","") 
            for name in sub.split("\\"):
                if name not in url_list:
                    url_list.append(name)
    
    return url_list
                
                
    
async def main():
    filename = "exploit.txt"
    start = 'exploit.to'
    final = {}
    tasks = []
    resolver = aiodns.DNSResolver()
    
    urls = get_urls(start)
    
    async with aiohttp.ClientSession() as session:
        for url in urls:
            tasks.append(fetch(session, url))
            tasks.append(query(resolver, url.replace("http://","").replace("https://",""), 'A'))
        statuses = await asyncio.gather(*tasks)
        for status in statuses:
            domain = status[0].replace("http://","").replace("https://","")
            if len(str(status[1])) == 3 or status[1] is None:
                final[domain] = {
                    "status" : status[1],
                    "ip" : final[domain].get("ip") if domain in final else None,
                }
            if len(str(status[1])) > 4:
                final[domain] = {
                    "status" : final[domain].get("status") if domain in final else None,
                    "ip" : status[1]
                }       
                
    for d in final:
        with open(filename, 'a') as out:
            out.write(f"{d},{final[d].get('status')},{final[d].get('ip')}" + '\n')
    



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())



