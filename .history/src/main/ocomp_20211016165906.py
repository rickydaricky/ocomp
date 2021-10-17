import discord
from database import Database

db = Database()


class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

        tokens = message.content.split(' ')

        if len(tokens) == 0:
            return

        if tokens[0].startswith('!addme'):
            if len(tokens) != 2:
                await message.channel.send('{0.author.mention}, please use your command this way: \n!addme battle_id \nsuch as: !addme Exor#11705'.format(message))
                return
            
            print(message.author)
            nonactivity = await db.set_user(tokens[1], Stats.replace_hashtag(str(message.author)))
            if nonactivity == 0:
                await message.channel.send('{0.author.mention}, the battle_id you added entered could not be found'.format(message))
                return  
            elif nonactivity == 1:
                await message.channel.send('{0.author.mention}, the battle_id you added entered is set to private'.format(message))
                return  
            elif nonactivity == 2:
                await message.channel.send('{0.author.mention}, your battle_id was succesfully added to my memory!'.format(message))
                return 
                

        if tokens[0].startswith('!compare'):
            await message.channel.send('{0.author.mention}, please use your command this way: \n!compare user1 user2, such as: \n!compare Exor Bosco Ana'.format(message))
            return

        if tokens[0].startswith('!hero'):
            data = db.find_hero(message.author.mention, tokens[1])
            await message.channel.send(f'{message.author.mention}, here are your stats on {tokens[1]}: {data}')
            return

        # fetch(tokens)


client = MyClient()
client.run('ODk3OTA5MTcwODA2ODgyMzY1.YWchFA.0pbCHQYXEBylmoBWM_5lfh7G3fM')