
import requests
import json
from urllib.parse import urlparse
import socket

import requests, json

class crtshAPI(object):
    """crtshAPI main handler."""

    def search(self, domain, wildcard=True, expired=True):
        """
        Search crt.sh for the given domain.

        domain -- Domain to search for
        wildcard -- Whether or not to prepend a wildcard to the domain
                    (default: True)
        expired -- Whether or not to include expired certificates
                    (default: True)

        Return a list of objects, like so:

        {
            "issuer_ca_id": 16418,
            "issuer_name": "C=US, O=Let's Encrypt, CN=Let's Encrypt Authority X3",
            "name_value": "hatch.uber.com",
            "min_cert_id": 325717795,
            "min_entry_timestamp": "2018-02-08T16:47:39.089",
            "not_before": "2018-02-08T15:47:39"
        }
        """
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


def is_url(url):
  try:
    result = urlparse(url)
    return all([result.scheme, result.netloc])
  except ValueError:
    return False

# Replace this domain.
site_infos = crtshAPI().search('exploit.to')

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
                
live_urls = []       
for url in url_list:
    
    try:
        ip = socket.gethostbyname(url)
    except Exception:
        ip = None
        pass

    try:
        url = "http://"+url.replace("*.","")
        is_available = requests.head(url, timeout=2).status_code
    except Exception:
        is_available = False
    live_urls.append((url,ip,is_available))
    
    print(f"Status:{is_available} IP:{ip} URL:{url}")
