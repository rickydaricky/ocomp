"""Modules imports: discord and database items"""
from database import replace_last_char, search_prefix, \
    replace_prefix, leave_guild, hero_word_match, \
    refresh_top100, set_user, find_hero, user_top_match
from discord.ext import commands
from discord.ext import tasks
from discord_slash import SlashCommand


async def get_prefix(_, message):
    """Retrieves the prefix the bot is listening to with the message as a context."""
    return await search_prefix(str(message.guild.id))

bot = commands.Bot(command_prefix=get_prefix)
slash = SlashCommand(bot, sync_commands=True)


@bot.event
async def on_ready():
    """
    Prints that the bot is logged on once it's logged on
    """
    print(f'Logged on as {bot.user.name}!')
    await refresh_top100()
    print('\ndone!')


@tasks.loop(minutes=5)
async def refresh_ranks():
    """Refreshes the list of the top 100 players in the world"""
    await refresh_top100()
    print('\ndone on interval!')


@bot.event
async def on_guild_join(guild):
    """Sets the default prefix to period"""
    await replace_prefix(str(guild.id), '.')


@bot.event
async def on_guild_remove(guild):
    """Removes the server from the database"""
    await leave_guild(str(guild.id))


# The following functions are bot commands, with each given a slash command counterpart.
# Slash commands are not yet implemented in discord.py so the implementation for both
# can't be put under the same function, but this will be updated once it has been.


@bot.command(name='commands', help='Lists all the commands I know!')
async def com(ctx):
    """Sends out a text guide on the available commands"""

    await ctx.send(f'{ctx.author.mention}, '
                   f'these are the available commands:\n'
                   f'`.addme [BattleTag]` :: '
                   'adds your BattleTag to my memory!\n'
                   f'`.hero [hero_name]` :: '
                   'displays your competitive stats on a partiular hero\n'
                   f'`.compare [discord_user_1] [discord_user_2] [hero_name]` '
                   ':: compares two players\' stats on a particular hero')


@slash.slash(name='commands', description='Lists all the commands I know!')
async def com_slash(ctx):
    """Sends out a text guide on the available commands.
    Slash version.
    """

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


@slash.slash(name='prefix', description='Changes my prefix to whatever you want!')
async def changeprefix_slash(ctx, new_prefix):
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

    nonactivity = await set_user(str(ctx.guild.id), args[0],
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


@slash.slash(name='addme', description='Adds the battle ID to the discord user in the database')
async def addme_slash(ctx, battle_id):
    """Adds the listed battle id to the discord user in the database.
    Slash version.
    """

    nonactivity = await set_user(str(ctx.guild.id), battle_id,
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


@bot.command(help='Compares the stats of the two listed players from the database.\n'
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
        data = await compare(str(ctx.guild.id), args[0], args[1], hero)
        player_1_hashtag = replace_last_char(await user_top_match(
            args[0]), '-', '#')
        player_2_hashtag = replace_last_char(await user_top_match(
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


@slash.slash(name='compare', description='Compares the stats '
             'of the two listed players from the database.')
async def compare_slash(ctx, user_1, user_2, hero_name):
    """Compares the stats of the two listed players from the database.
    Slash version."""

    try:
        hero = hero_name.lower()
        data = await compare(str(ctx.guild.id), user_1, user_2, hero)
        player_1_hashtag = replace_last_char(await user_top_match(
            user_1), '-', '#')
        player_2_hashtag = replace_last_char(await user_top_match(
            user_2), '-', '#')
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
        await ctx.send(f'{ctx.author.mention}, {err}')
        return


@bot.command(name='hero', help='Shows your stats on a specific hero!\n'
             f'Usage:\n{get_prefix}hero [hero_name], such as:'
             f'\n{get_prefix}hero ana')
async def single_hero_stats(ctx, hero_name):
    """Shows the stats of the calling discord user on a specific hero"""

    try:
        data = await find_hero(str(ctx.guild.id), replace_last_char(
            str(ctx.message.author), '#', '-'), hero_name.lower())
        if data == 'error':
            return
        await ctx.send(f'{ctx.message.author.mention}, '
                       f'here are your stats on {hero_word_match(hero_name)} per 10: {data}')
        return
    except ValueError:
        await ctx.send(f'{ctx.message.author.mention}, {hero_name} is not a valid hero name!.')
        return
    except AttributeError:
        try:
             hero_word_match(hero_name)
             
        await ctx.send(f'{ctx.message.author.mention}, you have not '
                       'added yourself to my database yet! '
                       'Please use the addme command first.')
        return


@slash.slash(name='hero', description='Shows your stats on a specific hero!')
async def single_hero_stats_slash(ctx, hero_name):
    """Shows the stats of the calling discord user on a specific hero.
    Slash version
    """

    try:
        data = await find_hero(str(ctx.guild.id), replace_last_char(
            str(ctx.message.author), '#', '-'), hero_name.lower())
        if data == 'error':
            return
        await ctx.send(f'{ctx.message.author.mention}, '
                       f'here are your stats on {hero_word_match(hero_name)} per 10: {data}')
        return
    except ValueError as err:
        await ctx.send(f'{ctx.author.mention}, {err}')
        return
    except AttributeError:
        await ctx.send(f'{ctx.author.mention}, you have not '
                       'added yourself to my database yet! '
                       'Please use the addme command first.')
        return


bot.run('ODk3OTA5MTcwODA2ODgyMzY1.YWchFA.0pbCHQYXEBylmoBWM_5lfh7G3fM')
