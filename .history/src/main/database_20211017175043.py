"""Program Modules: Regex, Firebase, Web Requests, and BeautifulSoup"""
import re
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import requests
from bs4 import BeautifulSoup


hero_list = ['ana', 'ashe', 'baptiste', 'bastion', 'brigitte', 'dva', 'doomfist',
             'echo', 'genji', 'hanzo', 'junkrat', 'lucio', 'mccree', 'mei', 'mercy', 'moira',
             'orisa', 'pharah', 'reaper', 'reinhardt', 'roadhog', 'sigma', 'soldier76', 'sombra',
             'symmetra', 'torbjorn', 'tracer', 'widowmaker', 'winston',
             'wreckingball', 'zarya', 'zenyatta']

cred = credentials.Certificate(
    "/Users/rickydaricky/Desktop/ocomp/overbuff-compare-firebase-adminsdk-h8051-7f0b808aa7.json")
firebase_admin.initialize_app(
    cred, {'databaseURL': 'https://overbuff-compare-default-rtdb.firebaseio.com'})
ref = db.reference("/Users")

try_header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
}


class Database():

    @staticmethod
    def dict_zip(*dicts):
        """Zip equivalent for dictionaries, with padding option. 
        Based off an implementation from Skyrill here:
        codereview.stackexchange.com/questions/160582/creating-zip-but-for-dictionaries
        """
        return {k: [d[k] for d in dicts] for k in dicts[0].keys()}

    async def set_user(self, battle_id, nickname):
        """Adds a player's battle_id to to their discord tag
        """
        nonactivity = await not_active(battle_id)
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

    async def user_match(self, nickname):
        """matches an abbreviated nickname to a list of users in the database
        """
        snapshot = ref.get()
        users_list = []
        for key, _ in snapshot.items():
            users_list.append(key)
        return word_match(nickname, users_list)

    async def find_hero_data(self, nickname, hero):
        """Looks for a hero in the given player's stats page.
        """
        battle_id = ''
        snapshot = ref.get()
        real_name = await Database.user_match(self, nickname)
        for key, val in snapshot.items():
            if key == real_name:
                battle_id = list(val.values())[0]
        if battle_id == '':
            raise ValueError('a user was not found in database')

        return await crawl_search_hero(battle_id, word_match(hero, hero_list))

    async def find_hero(self, nickname, hero):
        """Returns data (in a string) for a player's stats on a specific hero
        """
        results = await Database.find_hero_data(self, nickname, hero)
        response = ''
        for key, val in results.items():
            response += '\n' + key + ': ' + val
        return response

    async def compare(self, p1, p2, hero):
        """Compares 2 players's overbuff stats on a particular hero
        """
        response = ''

        p1_data = await Database.find_hero_data(self, p1, hero)
        p2_data = await Database.find_hero_data(self, p2, hero)
        try:
            for key, val in Database.dict_zip(p1_data, p2_data).items():
                val_1 = val[0]
                val_2 = val[1]
                if (key != 'Deaths' and val_1 > val_2) or (key == 'Deaths' and val_1 < val_2):
                    stat_status = f'\n{key}: **{val_1}**   ----   {key}: {val_2}'
                elif (key != 'Deaths' and val_1 < val_2) or (key == 'Deaths' and val_1 > val_2):
                    stat_status = f'\n{key}: {val_1}  ----   {key}: **{val_2}**'
                else:
                    stat_status = f'\n{key}: {val_1}  ----   {key}: {val_2}'
                response += stat_status
            return response
        except AttributeError:
            raise ValueError(
                'one of these players has not played this hero this season!')


def word_match(word, word_list):
    """Checks if any of the words in word_list start with the input word, and if there is only one, return that full word.
    Case insensitive.
    """
    possibles = []
    for w in word_list:
        if bool(re.match(word, w, re.I)):
            possibles.append(w)
    length_possibles = len(possibles)
    if length_possibles != 1:
        raise ValueError(
            'no hero could be found with that name, and it does not appear to be an abbreviation either')
    return possibles[0]


def replace_hashtag(battle_id):
    """Converts a battle id to a url based on that battle id"""
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


def id_to_url(battle_id):
    """
    converts a battle id to a url based on that battle id
    """
    print(battle_id)
    return 'https://www.overbuff.com/players/pc/' + replace_hashtag(battle_id) + '?mode=competitive'


async def crawl_search_hero(battle_id, hero):
    """
    Searches a player's page for stats on one of their heroes
    """
    responses = {}
    overbuff_url = id_to_url(battle_id)
    r = requests.get(overbuff_url, headers=try_header)
    soup = BeautifulSoup(r.content, 'html5lib')
    hero_response_list = soup.findAll(class_='theme-hero-' + hero)
    if not hero_response_list:
        return
    hero_response = hero_response_list[0]
    padded_stats = hero_response.findAll(class_='stat')
    for stat in padded_stats:
        children = stat.contents
        responses[children[len(children) - 1].text] = children[0].text
    return responses


async def not_active(battle_id):
    """
    Checks if a battle_id is real
    """
    overbuff_url = id_to_url(battle_id)
    r = requests.get(overbuff_url, headers=try_header)
    soup = BeautifulSoup(r.content, 'html5lib')
    layout_error = soup.find_all(class_='layout-error')
    private_error = soup.body.findAll(text='No QUICKPLAY Game Data Available')
    if len(layout_error) > 0:
        return 0
    elif len(private_error) > 0:
        return 1
    else:
        return 2
