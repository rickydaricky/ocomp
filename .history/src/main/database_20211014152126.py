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
        if (await Stats.not_active(battle_id)) == None:
            print("active")
            return
        else:
            print("not active")
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

        process = CrawlerProcess()
        process.crawl(Overbuff404Crawler, url = overbuff_url)
        global initialized
        print(initialized)
        if (not initialized):
            initialized = True
            process.start()


class Overbuff404(scrapy.Item):
    user_not_found = scrapy.Field()
        
class Overbuff404Crawler(scrapy.Spider):
    name = 'User Not Found Spider'
    allowed_domains = ['www.overbuff.com/players/pc/']
    start_urls = []
    def __init__(self, url=None, *args, **kwargs):
        super(Overbuff404Crawler, self).__init__(*args, **kwargs)
        self.start_urls = [f'{url}']

    def parse(self, response):
        item = Overbuff404()
        print(f"\nSTART URLS: {self.start_urls}\n")

        if response.status == 404:
            item['user_not_found'] = True
        else:
            print(response.css(".layout_error::text").getall())
            item['user_not_found'] = False
            # response.css(".layout_error::text").getall()

        return item

        # if len(response.css(".layout_error::text").getall()) > 0:
        #     print(len(response.css(".layout_error::text").getall()))
        #     print("\n\n\nREAD\n\n\n")
        #     yield [True]
        # yield [False]
        