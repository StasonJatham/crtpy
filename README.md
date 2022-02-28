# crtpy

Quick script to scrape https://crt.sh and check if service still online via HEAD request.
Please don't use this on too many targets as this is using an offical API. If you want to do bulk, consider making your own crt.sh with https://github.com/SSLMate/certspotter 

This is using Certificate Transparency for quick passive recon on a target to find old possibly forgotten endpoints.

## Usage 
Change the line i commented in the code and run. 
Output:
```
Status:301 IP:185.199.109.153 URL:http://www.exploit.to
Status:False IP:None URL:http://exploit.to
www.exploit.to
Status:False IP:None URL:http://drv.exploit.to
Status:301 IP:185.199.111.153 URL:http://exploit.to
Status:301 IP:104.22.62.243 URL:http://sni.cloudflaressl.com
```
