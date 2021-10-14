import discord
from database import Database

db = Database()


class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

        tokens = message.content.split(' ')

        if tokens[0].startswith('#add'):
            if tokens.size() != 3:
                await message.channel.send('{0.author.mention}, please use your command this way: !add battle_id your_own_nickname (case sensitive), such as !add Exor#11705 Exor'.format(message))
                return
            
            db.add(tokens[1], tokens[2])


        if tokens.size() < 4 and tokens[0].startswith('#compare'):
            await message.channel.send('{0.author.mention}, please use your command this way: !compare user1 user2, such as !compare Exor Bosco Ana'.format(message))
            return

        # fetch(tokens)


client = MyClient()
client.run('ODk3OTA5MTcwODA2ODgyMzY1.YWchFA.0pbCHQYXEBylmoBWM_5lfh7G3fM')