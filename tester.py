import requests

proxies=open('proxies.txt', 'r').read().split("\n")
proxies=[x for x in proxies if x!=""]

for pro in proxies:
    try:
        r=requests.get("https://linkedin.com/",proxies={"http":f"http://{pro}","https":f"http://{pro}"},timeout=10)
        print(pro)
    except:
        pass    

