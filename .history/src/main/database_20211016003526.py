import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import requests
from bs4 import BeautifulSoup

import json
import os


initialized = False

cred = credentials.Certificate("/Users/rickydaricky/Desktop/ocomp/overbuff-compare-firebase-adminsdk-h8051-7f0b808aa7.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://overbuff-compare-default-rtdb.firebaseio.com'})
ref = db.reference("/Users")



class Database():

    async def set_user(self, battle_id, nickname):
        if (await Stats.not_active(battle_id)):
            print("not active")
            return
        else:
            print("active")
            return


        ref.set({nickname: {'battle_id': battle_id}})

class Stats():
    
    async def not_active(battle_id):
        split_battle_id = list(battle_id)
        index = 0
        hashtag_index = -1
        for char in battle_id:
            if char == '#':
                hashtag_index = index
            index += 1
        if hashtag_index == -1:
            return True

        split_battle_id[hashtag_index] = '-'
        overbuff_battle_id = "".join(split_battle_id)

        overbuff_url = 'https://www.overbuff.com/players/pc/' + overbuff_battle_id + '?mode=competitive'

        intended_headers = {
            "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 
            "Accept-Encoding": 'gzip, deflate', 
            "Accept-Language": 'en-GB,en-US;q=0.9,en;q=0.8', 
            "Dnt": '1', 
            "Host": 'httpbin.org', 
            "Upgrade-Insecure-Requests": '1', 
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36', 
            }

        print(overbuff_url)
        r = requests.get(overbuff_url, headers = intended_headers)
        soup = BeautifulSoup(r.content, 'html5lib')
        layout_error = soup.find_all(class_ = 'layout_error')
        print(r.content)
        print(layout_error)
        return len(layout_error) > 0

        # f = open('items.json')
        # data = json.load(f)
        # user_not_found = data[0]['user_not_found']
        # f.close()

        # filePath = 'items.json'

        # if os.path.exists(filePath):
        #     os.remove(filePath)

        return user_not_found


