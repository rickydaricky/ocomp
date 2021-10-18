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

try_header = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36", 
        }



class Database():

    """
    Zip equivalent for dictionaries, with padding option. 
    Based off an implementation from Skyrill here: codereview.stackexchange.com/questions/160582/creating-zip-but-for-dictionaries
    """
    def dict_zip(*dicts, fillvalue=None):
        all_keys = {k for d in dicts for k in d.keys()}
        return {k: [d.get(k, fillvalue) for d in dicts] for k in all_keys}

    """
    Adds a player's battle_id to to their discord tag
    """
    async def set_user(self, battle_id, nickname):
        nonactivity = await Stats.not_active(battle_id)
        if nonactivity == 0:
            print('Battle_ID not found')
            return 0
        elif nonactivity == 1:
            print('private profile')
            return 1
        else:
            print("active")
            ref.set({nickname: {'battle_id': battle_id}})
            return 2

    """
    Looks for a hero in the given player's stats page.
    """

    async def find_hero_data(self, nickname, hero):
        battle_id = ''
        snapshot = ref.get()
        for key, val in snapshot.items():
            if key == nickname:
                battle_id = list(val.values())[0]
        if battle_id == '':
            print('user does not exist')
            return 0
        
        return await Stats.crawl_search_hero(battle_id, hero)

    async def find_hero(self, nickname, hero):
        results = await Database.find_hero_data(self, nickname, hero)
        response = ''
        for key, val in results.items():
            response += '\n' + key + ': ' + val
        return response

    """
    Compares 2 players's overbuff stats on a particular hero
    """
    async def compare(self, p1, p2, hero):
        response = ''
        p1_data = Database.find_hero_data(p1, hero)
        p2_data = Database.find_hero_data(p2, hero)
        for key, val in Database.dict_zip(p1_data, p2_data).items():
            val_1 = val[0]
            val_2 = val[1]
            if val_1 > val_2:
                stat_status = f'\n{key}: **{val_1}**   |||   {key}: {val_2}'
            elif val_1 < val_2:
                stat_status = f'\n{key}: {val_1}  |||   {key}: **{val_2}**'
            else:
                stat_status = f'\n{key}: {val_1}  |||   {key}: {val_2}'
            response += '\n' + key + ': ' + val_1 + '   |||   ' + key + ': ' + val_2
        return response
                
                


        # for key, val in dict_zip()
        


class Stats():

    """
    converts a battle id to a url based on that battle id
    """
    @staticmethod
    def replace_hashtag(battle_id):
        split_battle_id = list(battle_id)
        index = 0
        hashtag_index = -1
        for char in battle_id:
            if char == '#':
                hashtag_index = index
            index += 1
        if hashtag_index == -1:
            return battle_id

        split_battle_id[hashtag_index] = '-'
        return "".join(split_battle_id)

    """
    converts a battle id to a url based on that battle id
    """
    @staticmethod
    def id_to_url(battle_id):
        print(battle_id)
        return 'https://www.overbuff.com/players/pc/' + Stats.replace_hashtag(battle_id) + '?mode=competitive'


    """
    Searches a player's page for stats on one of their heroes
    """
    async def crawl_search_hero(battle_id, hero):

        responses = {}
        overbuff_url = Stats.id_to_url(battle_id)
        r = requests.get(overbuff_url, headers = try_header)
        soup = BeautifulSoup(r.content, 'html5lib')
        hero_response_list = soup.findAll(class_ = 'theme-hero-' + hero)
        if hero_response_list:
            return 'error hero not found'
        hero_response = hero_response_list[0]
        # print('Hero Response: ' + str(hero_response))
        padded_stats = hero_response.findAll(class_ = 'stat')
        # print('Padded: ' + str(padded_stats))
        for stat in padded_stats:
            children = stat.contents
            responses[children[len(children) - 1].text] = children[0].text
        # print('Responses: ' + str(responses))
        return responses


        

            
    

    """
    Checks if a battle_id is real
    """
    async def not_active(battle_id):
        overbuff_url = Stats().id_to_url(battle_id)

        intended_headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
            "Accept-Encoding": "gzip, deflate, br", 
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7", 
            "Host": "httpbin.org", 
            "Referer": "https://www.scrapehero.com/", 
            "Sec-Ch-Ua": "\"Chromium\";v=\"94\", \"Google Chrome\";v=\"94\", \";Not A Brand\";v=\"99\"", 
            "Sec-Ch-Ua-Mobile": "?0", 
            "Sec-Ch-Ua-Platform": "\"macOS\"", 
            "Sec-Fetch-Dest": "document", 
            "Sec-Fetch-Mode": "navigate", 
            "Sec-Fetch-Site": "cross-site", 
            "Sec-Fetch-User": "?1", 
            "Upgrade-Insecure-Requests": "1", 
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36", 
            "X-Amzn-Trace-Id": "Root=1-616a55cb-2eb5ed9c252af9804d974105"
            }

        r = requests.get(overbuff_url, headers = try_header)
        soup = BeautifulSoup(r.content, 'html5lib')
        layout_error = soup.find_all(class_ = 'layout-error')
        private_error = soup.body.findAll(text='No QUICKPLAY Game Data Available')
        if len(layout_error) > 0:
            return 0
        elif len(private_error) > 0:
            return 1
        else:
            return 2