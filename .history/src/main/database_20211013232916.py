import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("/Users/rickydaricky/Desktop/OverbuffCompare/overbuff-compare-firebase-adminsdk-h8051-7f0b808aa7.json")
firebase_admin.initialize_app(cred)