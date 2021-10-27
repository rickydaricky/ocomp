"""Modules imports: discord and database items"""
import discord
from database import Database, replace_last_char
from discord.ext import commands

db = Database()
bot = commands.Bot(command_prefix='.')


@bot.event
async def on_ready():
    """
    Prints that the bot is logged on once it's logged on
    """
    print(f'Logged on as {bot.user.name}!')
    await db.refresh_top100()
    print('\ndone!')


@bot.command(name='commands', help='Lists all the commands I know!')
async def com(ctx):
    """Sends out a text guide on the available commands"""

    await ctx.send(f'{ctx.message.author.mention}, '
                   f'these are the available commands:\n'
                   f'`.addme [BattleTag]` :: '
                   'adds your BattleTag to my memory!\n'
                   f'`.hero [hero_name]` :: '
                   'displays your competitive stats on a partiular hero\n'
                   f'`.compare [discord_user_1] [discord_user_2] [hero_name]` '
                   ':: compares two players\' stats on a particular hero')


@bot.command(help='Adds the battle ID to the discord user in the database\n'
             'usage: !addme battle_id \nsuch as: '
             '!addme Exor#11705')
async def addme(ctx, *args):
    """Adds the listed battle id to the discord user in the database"""
    if len(args) != 1:
        await ctx.send('{0.author.mention}, please use your command this way:'
                       ' \n!addme battle_id \nsuch as: '
                       '!addme Exor#11705'.format(ctx.message))
        return

    print(ctx.message.author)
    nonactivity = await db.set_user(args[0],
                                    replace_last_char(str(ctx.message.author), '#', '-'))
    if nonactivity == 0:
        await ctx.send('{0.author.mention}, '
                       'the battle_id you added entered '
                       'could not be found'.format(ctx.message))
        return
    if nonactivity == 1:
        await ctx.send('{0.author.mention}, '
                       'the battle_id you added entered '
                       'is set to private'.format(ctx.message))
        return
    if nonactivity == 2:
        await ctx.send('{0.author.mention}, '
                       'your battle_id was succesfully '
                       'added to my memory!'.format(ctx.message))
        return


@bot.command(help='')
async def compare(ctx, *args):
     if len(args) != 3:
            await message.channel.send('{0.author.mention}, '
                                       'please use your command this way: '
                                       '\n!compare user1 user2, such as: '
                                       '\n!compare Exor Bosco Ana'.format(message))
            return
        try:
            hero = args[2].lower()
            data = await db.compare(tokens[1], tokens[2], hero)
            player_1_hashtag = replace_last_char(await Database.user_match(
                args[0]), '-', '#')
            player_2_hashtag = replace_last_char(await Database.user_match(
                args[1]), '-', '#')
            len_1 = len(player_1_hashtag)
            space_gap = ' ' * max(0, round(1.8 * (25 - len_1)))
            await message.channel.send(f'{message.author.mention}, here is how '
                                       f'{player_1_hashtag} '
                                       f'and {player_2_hashtag}'
                                       f' match up on {hero}:\n\n'
                                       f'{player_1_hashtag}'
                                       f'{space_gap}----               '
                                       f'{player_2_hashtag}'
                                       f'\n------------------------------'
                                       f'-----------------------------------{data}')
            return
        except ValueError as err:
            await message.channel.send(f'{message.author.mention}, {err}')
            return

async def on_message(message):
    """
    Bot REPL
    """
    print('Message from {0.author}: {0.content}'.format(message))

    tokens = message.content.split(' ')

    if len(tokens) == 0:
        return

    if tokens[0].startswith('.compare'):
       

    if tokens[0].startswith('.hero'):
        data = await db.find_hero(replace_last_char(str(message.author),
                                                    '#', '-'), tokens[1].lower())
        if data == 'error':
            return
        await message.channel.send(f'{message.author.mention}, '
                                   f'here are your stats on {tokens[1]} per 10: {data}')
        return


bot.run('ODk3OTA5MTcwODA2ODgyMzY1.YWchFA.0pbCHQYXEBylmoBWM_5lfh7G3fM')
