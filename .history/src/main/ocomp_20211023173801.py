"""Modules imports: discord and database items"""
import discord
from database import Database, replace_last_char

db = Database()


class MyClient(discord.Client):
    """
    Runs the discord bot and keeps it active.
    Implements the repl as well.
    """

    async def on_ready(self):
        """
        Prints that the bot is logged on once it's logged on
        """
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        """
        Bot REPL
        """
        print('Message from {0.author}: {0.content}'.format(message))

        tokens = message.content.split(' ')

        if len(tokens) == 0:
            return

        if tokens[0].startswith('.addme'):
            if len(tokens) != 2:
                await message.channel.send('{0.author.mention}, please use your command this way:'
                                           ' \n!addme battle_id \nsuch as: '
                                           '!addme Exor#11705'.format(message))
                return

            print(message.author)
            nonactivity = await db.set_user(tokens[1],
                                            replace_last_char(str(message.author), '#', '-'))
            if nonactivity == 0:
                await message.channel.send('{0.author.mention}, '
                                           'the battle_id you added entered '
                                           'could not be found'.format(message))
                return
            elif nonactivity == 1:
                await message.channel.send('{0.author.mention}, '
                                           'the battle_id you added entered '
                                           'is set to private'.format(message))
                return
            elif nonactivity == 2:
                await message.channel.send('{0.author.mention}, '
                                           'your battle_id was succesfully '
                                           'added to my memory!'.format(message))
                return

        if tokens[0].startswith('.compare'):
            if len(tokens) != 4:
                await message.channel.send('{0.author.mention}, '
                                           'please use your command this way: '
                                           '\n!compare user1 user2, such as: '
                                           '\n!compare Exor Bosco Ana'.format(message))
                return
            try:
                data = await db.compare(tokens[1], tokens[2], tokens[3].lower())
                player_1_hashtag = replace_last_char(await Database.user_match(
                    self, tokens[1]), '-', '#')
                player_2_hashtag = replace_last_char(await Database.user_match(
                    self, tokens[2]), '-', '#')
                len_1 = len(player_1_hashtag)
                space_gap = ' ' * max(0, round(1.8 * (25 - len_1)))
                await message.channel.send(f'{message.author.mention}, here is how '
                                           f'{player_1_hashtag} '
                                           f'and {player_2_hashtag}'
                                           ' match up:\n\n'
                                           f'{player_1_hashtag}'
                                           f'{space_gap}----               '
                                           f'{player_2_hashtag}'
                                           f'\n------------------------------'
                                           f'------------------------------{data}')
                return
            except ValueError as err:
                await message.channel.send(f'{message.author.mention}, {err}')
                return

        if tokens[0].startswith('.hero'):
            data = await db.find_hero(replace_last_char(str(message.author),
                                                        '#', '-'), tokens[1].lower())
            if data == 'error':
                return
            await message.channel.send(f'{message.author.mention}, '
                                       f'here are your stats on {tokens[1]} per 10: {data}')
            return


client = MyClient()
client.run('ODk3OTA5MTcwODA2ODgyMzY1.YWchFA.0pbCHQYXEBylmoBWM_5lfh7G3fM')
