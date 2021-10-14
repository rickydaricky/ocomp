import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import scrapy


cred = credentials.Certificate("/Users/rickydaricky/Desktop/OverbuffCompare/overbuff-compare-firebase-adminsdk-h8051-7f0b808aa7.json")
firebase_admin.initialize_app(cred)
ref = db.reference("/Users")

class Database():

    async def add(battle_id, nickname):



        ref.set({nickname: {'battle_id': battle_id}})
