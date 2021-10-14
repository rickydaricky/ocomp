import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import scrapy


cred = credentials.Certificate("/Users/rickydaricky/Desktop/OverbuffCompare/overbuff-compare-firebase-adminsdk-h8051-7f0b808aa7.json")
firebase_admin.initialize_app(cred)
ref = db.reference("/Users")

class Database():

    async def add(battle_id, nickname):
        if (Stats.not_active(battle_id)):
            return


        ref.set({nickname: {'battle_id': battle_id}})

@staticmethod
class Stats():

    async def not_active(battle_id):
        overbuff_battle_id = ""
        index = 0
        hashtag_index = -1
        for char in battle_id:
            if char == '#':
                hashtag_index = index
            index += 1


        url = 'overbuff.com/players/pc/Exor-11705' + hashtag_index
