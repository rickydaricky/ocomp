"""Modules imports: discord and database items"""
from database import Database, replace_last_char, search_prefix, replace_prefix, join_guild, leave_guild
from discord.ext import commands

db = Database()


async def get_prefix(bot, message):
    """Retrieves the prefix the bot is listening to with the message as a context."""
    return await search_prefix(str(message.guild.id))

bot = commands.Bot(command_prefix=get_prefix)


@bot.event
async def on_ready():
    """
    Prints that the bot is logged on once it's logged on
    """
    print(f'Logged on as {bot.user.name}!')

    # await db.refresh_top100()
    # print('\ndone!')

@bot.event
async def on_guild_join(guild):
    join_guild(str(guild))

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


@bot.command(name='prefix', help='Changes my prefix to whatever you want!')
async def changeprefix(ctx, new_prefix):
    """Changes the bot prefix to the new_prefix"""

    replace_prefix(str(ctx.guild.id), new_prefix)
    await ctx.send(f'{ctx.message.author.mention}, '
                   'the prefix has been changed to {new_prefix}!')


@bot.command(help='Adds the battle ID to the discord user in the database\n'
             f'Usage:\n{get_prefix}addme battle_id \nsuch as: '
             f'{get_prefix}addme Exor#11705')
async def addme(ctx, *args):
    """Adds the listed battle id to the discord user in the database"""

    if len(args) != 1:
        await ctx.send('{0.author.mention}, please use your command this way:'
                       ' \n.addme battle_id \nsuch as: '
                       '.addme Exor#11705'.format(ctx.message))
        return

    nonactivity = await db.set_user(str(ctx.guild.id), args[0],
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


@ bot.command(help='Compares the stats of the two listed players from the database.\n'
              f'Usage:\n{get_prefix}compare user1 user2, such as: '
              f'\n{get_prefix}compare Exor Bosco Ana')
async def compare(ctx, *args):
    """Compares the stats of the two listed players from the database."""

    if len(args) != 3:
        await ctx.send('{0.author.mention}, '
                       'please use your command this way: '
                       '\n!compare user1 user2, such as: '
                       '\n!compare Exor Bosco Ana'.format(ctx.message))
        return
    try:
        hero = args[2].lower()
        data = await db.compare(str(ctx.guild.id), args[0], args[1], hero)
        player_1_hashtag = replace_last_char(await Database.user_match(
            args[0]), '-', '#')
        player_2_hashtag = replace_last_char(await Database.user_match(
            args[1]), '-', '#')
        len_1 = len(player_1_hashtag)
        space_gap = ' ' * max(0, round(1.8 * (25 - len_1)))
        await ctx.send(f'{ctx.message.author.mention}, here is how '
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
        await ctx.send(f'{ctx.message.author.mention}, {err}')
        return


@ bot.command(name='hero', help='Shows your stats on a specific hero!\n'
              f'Usage:\n{get_prefix}hero [hero_name], such as:'
              f'\n{get_prefix}hero ana')
async def single_hero_stats(ctx, *args):
    """Shows the stats of the calling discord user on a specific hero"""

    data = await db.find_hero(replace_last_char(str(ctx.guild.id), str(ctx.message.author),
                                                '#', '-'), args[0].lower())
    if data == 'error':
        return
    await ctx.send(f'{ctx.message.author.mention}, '
                   f'here are your stats on {args[0]} per 10: {data}')
    return

bot.run('ODk3OTA5MTcwODA2ODgyMzY1.YWchFA.0pbCHQYXEBylmoBWM_5lfh7G3fM')
