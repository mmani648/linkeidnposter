import requests
import json
import datetime
import pytz
import os
import shutil
import random


def poster(pro,links,token,cookies,zone,message):
        headers = {
            'authority': 'www.linkedin.com',
            'accept': 'application/vnd.linkedin.normalized+json+2.1',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7,pa;q=0.6,da;q=0.5',
            'content-type': 'application/json; charset=UTF-8',            
            'csrf-token': token,
            'origin': 'https://www.linkedin.com',
            'referer': 'https://www.linkedin.com/in/infobeckons-technologies/',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'cookie': "; ".join([str(x)+"="+str(y) for x,y in cookies.items()]),
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
            'x-li-lang': 'en_US',
          #  'x-li-page-instance': 'urn:li:page:d_flagship3_profile_view_base;BR6K/5vvQ/eLOq0nojDJ2g==',
            'x-li-track': '{"clientVersion":"1.10.8207","mpVersion":"1.10.8207","osName":"web","timezoneOffset":%s,"timezone":%s,"deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":1,"displayWidth":1920,"displayHeight":1080}'%(zone,timezone),
            'x-restli-protocol-version': '2.0.0',}

        s= requests.Session()
        s.headers.update(headers)
        s.proxies.update({"http":f"http://{pro}","https":f"http://{pro}"})
        print(s.get("http://ipinfo.io/ip").text)
    
   
        
        response = s.get('https://www.linkedin.com/mysettings-api/settingsApiMiniProfile')
        account=""  
        try:
            name1=response.json()['data']['firstName'] + ' ' + response.json()['data']['lastName']
            print(f"current account {name1}")
    
        except:
            shutil.move(f"cookies/{cook}",f"not/{cook}")
            account=None
        

        count=0
        if account!=None:
            for link in links:
                name=""
                try:
                    name=link.strip("/").split("/")[-1]
                    response = s.get(
                        f'https://www.linkedin.com/voyager/api/identity/profiles/{name}').json()
                    print(link)
                    pid = response['data']['entityUrn'].split("urn:li:fs_profile:")[1]
                    name = response['included'][0]['firstName'] + " " + response['data']['lastName']
                    name=name.strip()

                except:
                    
                    name=None
                    

                if name!=None:    
                    json_data = {
                            'visibleToConnectionsOnly': False,
                            'externalAudienceProviders': [],
                            'commentaryV2': {
                                'text': f'{name} {message}',
                                'attributes': [
                                    {
                                        'type': 'PROFILE_MENTION',
                                        'start': 0,
                                        'length': len(name),
                                        'normalizedProfileUrn': f'urn:li:fs_normalized_profile:{pid}',
                                    },
                                ],
                            },
                            'origin': 'FEED',
                            'allowedCommentersScope': 'ALL',
                            'postState': 'PUBLISHED',
                            'media': [],}
                    
                    response = s.post('https://www.linkedin.com/voyager/api/contentcreation/normShares', json=json_data)
               
                
                    if response.json()['data']['status']==429:

                        print("Account Temporary Disabled for Posting......  ")
                        break
                        
                    else:
                        # print(response.json())    
                        #  
                        try:     
                             
                            url_=response.json()['data']['status']['toastCtaUrl']
                            print(url_)
                        

                            if response.status_code==201:                
                                
                                count+=1
                                print(count) 
                            
                                with open("logs.txt","a+",encoding='utf-8') as f:
                                    f.write(f"{url_}\n")
                                if count==40:
                                    shutil.move(f"cookies/{cook}",f"storage/{cook}")
                                
                                        
                                    break
                                        
                            
                            else:
                                print(f"Post failed {link}")
                                with open("logs.txt","a+",encoding='utf-8') as f:
                                    f.write("|\n")
                        except:
                            print(response.json())     
                            print(f"Post failed {link}")
                            with open("logs.txt","a+",encoding='utf-8') as f:
                                f.write("|\n")













links=open("links.txt","r",encoding='utf-8').read().split("\n")
links=[x for x in links if x!=""]

msg1="thought it'd be nice to connect with others interested in eCommerce.  Any in-person conferences you're heading to soon?  Are you checking out this eCom Growth Livestream happening right now? Founders of 5 $1bn+ eComm brands are on deck. https://www.ecomlivestream.com/streaming-now"
msg2="thought it'd be nice to connect with others interested in eCommerce. Any in-person conferences you're heading to soon? Are you checking out this eCom Growth Livestream happening right now? Founders of 5 $1bn+ eComm brands are on deck. https://www.linkedin.com/video/event/urn:li:ugcPost:6991548949740290048/"
message=random.choice([msg1, msg2])


cookiess=os.listdir('cookies')
cookiess=[x for x in cookiess if x.endswith('.json')]
proxies=open('proxies.txt', 'r').read().split("\n")
proxies=[x for x in proxies if x!=""]

for cook,pro in zip(cookiess,proxies):
    print(cook)
    cookies=json.loads(open(f"cookies/{cook}","r").read())
    token=cookies['JSESSIONID'].strip('"')   
    try: timezone=cookies['timezone'] 
    except: timezone=cookies['timezone'] ="America/Los_Angeles"
    pacific_now = datetime.datetime.now(pytz.timezone(timezone))
    zone=pacific_now.utcoffset().total_seconds()/60/60
    if len(links)!=0:
        
        try:
            old=open('logs.txt','r',encoding='utf-8').read().split("\n")    
            links=open("links.txt","r",encoding='utf-8').read().split("\n")
            links=[x for x in links if x!=""]
            ln=len(old)
            links=links[ln:]
            print(len(links))        

            poster(pro,links,token,cookies,zone,message)
        except requests.exceptions.ProxyError as err:
            print("trying again proxy error")
            print(pro)
            pro=random.choice(proxies)
            try:
                poster(pro,links,token,cookies,zone,message)
            except:
                for _ in range(5):
                    print("retrying again  ",_)
                    pro=random.choice(proxies)
                    poster(pro,links,token,cookies,zone,message)
                    break

            

