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

        r = requests.get(overbuff_url)
        soup = BeautifulSoup(r.content, 'html5lib')


        # f = open('items.json')
        # data = json.load(f)
        # user_not_found = data[0]['user_not_found']
        # f.close()

        # filePath = 'items.json'

        # if os.path.exists(filePath):
        #     os.remove(filePath)

        return user_not_found


