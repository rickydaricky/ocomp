import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("/Users/rickydaricky/Desktop/OverbuffCompare/overbuff-compare-firebase-adminsdk-h8051-7f0b808aa7.json")
firebase_admin.initialize_app(cred)

class Database():
    ref = db.reference("/Users")
    