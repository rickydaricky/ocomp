# Ocomp
 
This is a simple discord bot that tracks your Overwatch stats and lets you compare yourself to your peers and top-ranked players. It's often incredibly annoying to compare stats between you and your friends in Career Profiles / in Overbuff, and this bot utilizes public Overbuff stats to make this tracking as simple as possible.

## How do I use it?

The bot supports slash commands, but its default prefix is "."

It supports 4 commands:
1. `.help`, which lists all the commands in simple terms
2. `.commands`, which is a more detailed version of `.help` that focuses on the primary commands.
3. `.addme` which takes in a BattleTag and stores your discord ID with that tag. Can be updated.
4. `.hero` which takes in a hero name (see below) and prints out your stats on that particular hero.
5. `.compare` which takes in a user1, a user2, a hero, and prints out both of your stats on those heroes. Can include players in the Top 100 Overbuff rankings. Example: ".compare lukemino ultraviolet ana"
6. `.prefix`, which takes in a new prefix and updates the current prefix accordingly. Only accessible to admins.

I highly encourage usage of slash commands in lieu of the traditional prefixes because they make the commands so much easier.

The hero names, based on Overbuff naming convention, are: 'ana', 'ashe', 'baptiste', 'bastion', 'brigitte', 'cassidy', 'dva', 'doomfist', 'echo', 'genji', 'hanzo', 'junkrat', 'lucio', 'mei', 'mercy', 'moira', 'orisa', 'pharah', 'reaper', 'reinhardt', 'roadhog', 'sigma', 'soldier76', 'sombra', 'symmetra', 'torbjorn', 'tracer', 'widowmaker', 'winston', 'wreckingball', 'zarya', 'zenyatta'


## How does it work?

Once you add yourself to your server-specific Ocomp database (stored in Firebase), it is able to convert your Battle ID into an Overbuff URL that it can then crawl and search (using BeautifulSoup) for your hero-specific stats.

## Notes

- I'll probably update the bot once Discord updates their Python api with native slash command support, since I'm currently using the discord_slash module.
- If the bot is down for whatever reason or you encounter any bugs, please contact me!
