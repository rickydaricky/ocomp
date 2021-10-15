import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import scrapy
from scrapy.crawler import CrawlerProcess

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


        ref.set({nickname: {'battle_id': battle_id}})

class Stats():

    async def not_active(battle_id):
        overbuff_battle_id = battle_id
        index = 0
        hashtag_index = -1
        for char in battle_id:
            if char == '#':
                hashtag_index = index
            index += 1
        if hashtag_index == -1:
            return True

        overbuff_battle_id[hashtag_index] == '-'

        overbuff_url = 'https://www.overbuff.com/players/pc/' + overbuff_battle_id + '?mode=competitive'

        process = CrawlerProcess()
        process.crawl(Overbuff404Crawler, url = overbuff_url)
        process.start()



        
class Overbuff404Crawler(scrapy.Spider):
    name = 'User Not Found Spider'
    allowed_domains = ['https://www.overbuff.com/players/pc/']
    start_urls = []

    initialized = True

    def __init__(self, url=None, *args, **kwargs):
        super(Overbuff404Crawler, self).__init__(*args, **kwargs)
        self.start_urls = [f'{url}']

    def parse(self, response):
        if len(response.css(".layout_error::text").getall()) > 0:
            print(len(response.css(".layout_error::text").getall()))
            return True
        return False
        