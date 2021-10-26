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
    """Instance of a database and supports database-related methods
    """

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
            ref.update({nickname: {'battle_id': battle_id}})
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

    @staticmethod
    async def refresh_top100():
        """Crawls through the top 100 players on
        overbuff and adds them to the database
        """
        top_url = 'https://www.overbuff.com/rankings'
        header_request = requests.get(top_url, headers=try_header)
        soup = BeautifulSoup(header_request.content, 'html5lib')
        player_response_list = soup.find(class_='table-condensed-mobile').contents[1]
        # print(player_response_list)
        # print('\n')
        for player in player_response_list:
            player_url = player.contents[0].contents[0]['href']
            player_id = player_url[12:]
            ref.update({player_id: {'battle_id': player_id}})

    async def compare(self, player_1, player_2, hero):
        """Compares 2 players's overbuff stats on a particular hero
        """
        response = ''

        p1_data = await Database.find_hero_data(self, player_1, hero)
        p2_data = await Database.find_hero_data(self, player_2, hero)

        spaces = ' ' * 15

        try:
            for key, val in Database.dict_zip(p1_data, p2_data).items():
                val_1 = val[0]
                val_2 = val[1]
                space_gap = ' ' * \
                    max(0, round(1.8 * (25 - len(val_1) - len(key))))

                # -1 means val_1 should be emphasized
                # 0 means equal
                # 1 means val_2 should be emphasized
                status = 0

                if 'Deaths' in key:
                    val_1_f = float(val_1)
                    val_2_f = float(val_2)
                    status = val_comp(val_2_f, val_1_f)
                elif key == 'Record':
                    status = 0
                elif key == 'Time Played':
                    val_1_vars = val_1.split(' ')
                    val_1_coef = val_1_vars[0]
                    val_1_unit = val_1_vars[1]
                    val_2_vars = val_2.split(' ')
                    val_2_coef = val_2_vars[0]
                    val_2_unit = val_2_vars[1]

                    if val_1_unit == val_2_unit:
                        status = val_comp(val_1_coef, val_2_coef)
                    else:
                        if val_1_unit == 'hours':
                            status = -1
                        elif val_2_unit == 'hours':
                            status = 1

                elif key == 'Hero Score ':
                    val_1_f = int(val_1.replace(',', ''))
                    val_2_f = int(val_2.replace(',', ''))
                    status = val_comp(val_1_f, val_2_f)
                elif key == 'Hero Rank':
                    if val_1 == '∞' or val_2 == '∞':
                        status = 0
                    elif '#' in val_1 and '#' in val_2:
                        val_1_f = int(val_1.replace('#', ''))
                        val_2_f = int(val_2.replace('#', ''))
                        status = val_comp(val_2_f, val_1_f)
                    elif '%' in val_1 and '%' in val_2:
                        val_1_f = int(val_1.replace('%', ''))
                        val_2_f = int(val_2.replace('%', ''))
                        status = val_comp(val_1_f, val_2_f)
                    else:
                        if '#' in val_1:
                            status = -1
                        else:
                            status = 1
                elif key == 'Win Rate':
                    val_1_f = float(val_1[:-2])
                    val_2_f = float(val_2[:-2])
                    status = val_comp(val_1_f, val_2_f)
                elif key == 'Final Blows' or key == 'Obj Kills' \
                    or key == 'Eliminations' or key == 'Destruct Kills':
                    val_1_f = float(val_1)
                    val_2_f = float(val_2)
                    status = val_comp(val_1_f, val_2_f)
                else:
                    status = val_comp(val_1, val_2)

                if status == 0:
                    stat_status = f'\n{key}: {val_1}{space_gap}----{spaces}{key}: {val_2}'
                elif status == -1:
                    stat_status = f'\n{key}: __**{val_1}**__{space_gap}----{spaces}{key}: {val_2}'
                elif status == 1:
                    stat_status = f'\n{key}: {val_1}{space_gap}----{spaces}{key}: __**{val_2}**__'

                response += stat_status
            return response
        except AttributeError as err:
            raise ValueError(
                'one of these players has not played this hero this season!') from err


def val_comp(val_1, val_2) -> str:
    """Compares two values and returns -1, 0, or 1
    depending on whether val_1 is greater than,
    equal to, or less than val_2"""
    status = 0
    if val_1 > val_2:
        status = -1
    elif val_1 < val_2:
        status = 1
    return status


def word_match(word, word_list):
    """Checks if any of the words in word_list start with the input word,
    and if there is only one, return that full word.
    Case insensitive.
    """
    possibles = []
    for item in word_list:
        if bool(re.match(word, item, re.I)):
            possibles.append(item)
    length_possibles = len(possibles)
    if length_possibles != 1:
        for item in possibles:
            if word == item.lower() or word == item[:item.find('-')].lower():
                return item
        print(f'\n{word}, {possibles}')
        raise ValueError(
            'no user or hero could be found with one of these names, '
            'and it does not appear to be an abbreviation either')
    return possibles[0]


def replace_last_char(battle_id, old_char, new_char):
    """Replaces the last specified char in a string with a new char.
    """
    split_battle_id = list(battle_id)
    index = 0
    hashtag_index = -1
    for char in battle_id:
        if char == old_char:
            hashtag_index = index
        index += 1
    if hashtag_index == -1:
        return battle_id

    split_battle_id[hashtag_index] = new_char
    return "".join(split_battle_id)


def id_to_url(battle_id):
    """Converts a battle id to a url based on that battle id
    """
    print(battle_id)
    url = ('https://www.overbuff.com/players/pc/'
           + replace_last_char(battle_id, '#', '-') + '?mode=competitive')
    return url


async def not_active(battle_id):
    """Checks if a battle_id is real
    """
    overbuff_url = id_to_url(battle_id)
    header_request = requests.get(overbuff_url, headers=try_header)
    soup = BeautifulSoup(header_request.content, 'html5lib')
    layout_error = soup.find_all(class_='layout-error')
    private_error = soup.body.findAll(text='No QUICKPLAY Game Data Available')
    if len(layout_error) > 0:
        return 0
    if len(private_error) > 0:
        return 1
    return 2


async def crawl_search_hero(battle_id, hero):
    """Searches a player's page for stats on one of their heroes
    """
    responses = {}
    overbuff_url = id_to_url(battle_id)
    header_request = requests.get(overbuff_url, headers=try_header)
    soup = BeautifulSoup(header_request.content, 'html5lib')
    hero_response_list = soup.findAll(class_='theme-hero-' + hero)
    if not hero_response_list:
        return
    hero_response = hero_response_list[0]
    padded_stats = hero_response.findAll(class_='stat')
    for stat in padded_stats:
        children = stat.contents
        responses[children[len(children) - 1].text] = children[0].text
    return responses
