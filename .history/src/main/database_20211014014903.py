import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import scrapy
from scrapy.crawler import CrawlerProcess

cred = credentials.Certificate("/Users/rickydaricky/Desktop/OverbuffCompare/overbuff-compare-firebase-adminsdk-h8051-7f0b808aa7.json")
firebase_admin.initialize_app(cred)
ref = db.reference("/Users")

current_link = ""

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
            return 0

        overbuff_battle_id[hashtag_index] == '-'

        url = 'www.overbuff.com/players/pc/' + overbuff_battle_id + '?mode=competitive'

        
class Overbuff404Crawler(scrapy.Spider):
    name = 'User Not Found Spider'
    allowed_domains = ['www.overbuff.com/players/pc/']
    start_urls = []

    # def __init__(self, *args, **kwargs): 
    #   super(Overbuff404Crawler, self).__init__(*args, **kwargs) 
    #   self.start_urls = [kwargs.get('start_url')]

    def parse(self, response):
        if len(response.css(".layout_error::text").getall()) > 0:
            return 1
        return 0
        
        
# process = CrawlerProcess(settings={
#     "FEEDS": {
#         "items.json": {"format": "json"},
#     },
# })

# process.crawl(Overbuff404Crawler)
# process.start()
