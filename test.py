import requests 
import pandas as pd
import csv
import json
from dotenv import load_dotenv 
import os

load_dotenv()

CLIENT_ID=os.getenv("CLIENT_ID")
SECRET_KEY=os.getenv("SECRET_KEY")

auth=requests.auth.HTTPBasicAuth(CLIENT_ID,SECRET_KEY)
data={
    'grant_type':'password',
    'username':os.getenv("USERNAME"),
    'password':os.getenv("PASSWORD")
}

headers={'User-Agent':'MyAPI/0.0.1'}
res=requests.post('https://www.reddit.com/api/v1/access_token',auth=auth,data=data,headers=headers)
TOKEN=res.json()['access_token']
headers={**headers, **{'Authorization':f'bearer {TOKEN}'}}

limit=input('***Limit nedir?***')
word=input('***Bir kelime giriniz?***')


def running(res):
    df=pd.DataFrame()
    for post in res.json()['data']['children']:
        js={}
        js['subreddit']=post['data']['subreddit']
        js['name']=post['data']['name']
        js['title']=post['data']['title']
        js['selftext']=post['data']['selftext']
        js['upvote_ratio']=post['data']['upvote_ratio']
        js['ups']=post['data']['ups']
        lastname=post['data']['name']
        with open(f'{word}.json','a') as ft:
            json.dump(js, ft)
            ft.write('\n')

    with open('pagination.csv','a') as fx:
        fx.writelines(f'{str(lastname)}\n')
       
    print(df)




with open('pagination.csv','a') as ftr:
    try:
        last_line = csv.reader(ftr)
        for satir in last_line:
            a=satir
        pagi=str(a).replace("['","").replace("']","")
        res=requests.get(f'https://oauth.reddit.com/r/{word}/new.json?limit={limit}&after={pagi}',headers=headers)
        running(res)
        print("TRY")
    except:
        res=requests.get(f'https://oauth.reddit.com/r/{word}/new.json?limit={limit}',headers=headers)
        last_line=res.json()['data']['children'][-1]['data']['name']
        running(res)
        print("except")



