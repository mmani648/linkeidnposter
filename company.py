from matplotlib.widgets import EllipseSelector
import requests
import json
import datetime
import pytz
import os
import shutil
from time import sleep

import random


def poster(pro,links,token,cookies,zone):

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
        
    s = requests.Session()
    s.headers.update(headers)
    
    proxy={"http":f"http://{pro}","https":f"http://{pro}"}

    s.proxies.update(proxy)
    print(s.get("http://ipinfo.io/ip").text)
    response = s.get('https://www.linkedin.com/mysettings-api/settingsApiMiniProfile',timeout=60)

    try:
        name=response.json()['data']['firstName'] + ' ' + response.json()['data']['lastName']
    except:
        name=None
    if name !=None:        

        
        print(f"current account {name}")
        count=0
        for link in links:
            print(link)
            
        
            name=link.strip("/").split("/")[-1]
        
            
            params = {
                        "decorationId": "com.linkedin.voyager.deco.organization.web.WebFullCompanyMain-12",
                        "q": "universalName",
                        "universalName":name,
                    }


            response = s.get('https://www.linkedin.com/voyager/api/organization/companies',params=params)

            
            open("data.json","w").write(json.dumps(response.json(),indent=4))
            try:
                data=response.json()
                name_com=""
                for i in data['included']:
                    if "name" in i:
                        name_com=i['name']
                print(name_com)
            
                try:
                    urn=response.json()['data']['*elements'][0].split("urn:li:fs_normalized_company:")[1]
                except:
                    urn=response.json()['data']['*elements'][0].split("urn:li:fs_followingInfo:urn:li:company:")[1]                
                print(urn)
                json_data  = {
                                'visibleToConnectionsOnly': False,
                                'externalAudienceProviders': [],
                                'commentaryV2': {
                                    'text':f"{name_com} {message}" ,
                                    'attributes': [
                                        {
                                            'type': 'COMPANY_NAME',
                                            'start': 0,
                                            'length': len(name_com),
                                            'normalizedCompanyUrn': f'urn:li:fs_normalized_company:{urn}',
                                        },
                                    ],
                                },
                                'origin': 'FEED',
                                'allowedCommentersScope': 'ALL',
                                'postState': 'PUBLISHED',
                                'media': [],
                                }

                response = s.post('https://www.linkedin.com/voyager/api/contentcreation/normShares',  json=json_data)
            
                if response.json()['data']['status']==429:

                    print("Account Temporary Disabled for Posting......  ")
                    break
                    
                else:
                # print(response.json())
                                
                    url_=response.json()['data']['status']['toastCtaUrl']
                    
                

                    if response.status_code==201:
                        print(url_)
                        with open("posts.txt","a+") as f:
                            f.write(f"{url_}\n")
                        count+=1
                    
                        print(count) 
                        if count==25:
                            shutil.move(f"cookies/{cook}",f"storage/{cook}")
                            
                            break
                                    
                        
                        with open("logs.txt","a+",encoding='utf-8') as f:
                            f.write(f"{url_}\n")
                    else:
                        print(f"Post failed {link}")

            
                        with open("logs.txt","a+",encoding='utf-8') as f:
                            f.write(f"|\n")
            except:
                pass            
    else:
        shutil.move(f"cookies/{cook}",f"not/{cook}")




links=open("links.txt","r",encoding='utf-8').read().split("\n")
links=[x for x in links if x!=""]

message="""Love your brand!  Are you guys speaking at any eCom conferences in ‘23?  ShopTalk?  NRF?  EcomLiveStream?  Hear they’re taking applications for January. Would love to hear someone from your brand speak https://www.ecomlivestream.com/apply-to-be-a-speaker"""

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
   
    try:
        old=open('logs.txt','r',encoding='utf-8').read().split("\n")    
        links=open("links.txt","r",encoding='utf-8').read().split("\n")
        links=[x for x in links if x!=""]
        ln=len(old)
        links=links[ln:]
        print(len(links))
        poster(pro,links,token,cookies,zone)
       
    except requests.exceptions.ProxyError as err:
        print("trying again proxy error")
        pro=random.choice(proxies)
        print(pro)
        
        poster(pro,links,token,cookies,zone)
       

    
        
        