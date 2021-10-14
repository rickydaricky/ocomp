import discord

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

        tokens = message.content.split(' ')
        
        if tokens.count() < 4:
            print('@{0.author}, please use  your command this way: !compare user1 user2, such as !compare Exor Bosco Ana', message)
            return

client = MyClient()
client.run('ODk3OTA5MTcwODA2ODgyMzY1.YWchFA.0pbCHQYXEBylmoBWM_5lfh7G3fM')