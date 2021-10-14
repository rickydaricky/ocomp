import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import scrapy
from scrapy.crawler import CrawlerProcess

cred = credentials.Certificate("/Users/rickydaricky/Desktop/OverbuffCompare/overbuff-compare-firebase-adminsdk-h8051-7f0b808aa7.json")
firebase_admin.initialize_app(cred)
ref = db.reference("/Users")

class Database():

    async def add(battle_id, nickname):
        if (Stats.not_active(battle_id)):
            return


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

        overbuff_url = 'www.overbuff.com/players/pc/' + overbuff_battle_id + '?mode=competitive'

        process = CrawlerProcess()
        process.crawl(Overbuff404Crawler, url = overbuff_url)
        return process.start()



        
class Overbuff404Crawler(scrapy.Spider):
    name = 'User Not Found Spider'
    allowed_domains = ['www.overbuff.com/players/pc/']
    start_urls = []

    def __init__(self, url=None, *args, **kwargs):
        super(Overbuff404Crawler, self).__init__(*args, **kwargs)
        self.start_urls = [f'{url}']

    def parse(self, response):
        if len(response.css(".layout_error::text").getall()) > 0:
            return True
        return False
        
        

