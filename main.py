from replayChecker import Checker
import Dbot as Dbot
from discord import Intents 


url = [
        "https://priconne-redive.us/profile/get_profile"
    ]

bot = Dbot.pvpBot(command_prefix='!')
bot.add_cog(Dbot.discordPVP(bot,url))
discordbot = Dbot.discordPVP(bot,url)
discordbot.start()


addons = [
    Checker(url, discordbot.ivKey) 
]
