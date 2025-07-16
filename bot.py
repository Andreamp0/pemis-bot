import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from keep_alive import keep_alive
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
keep_alive()
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='.', intents=intents)
bot.remove_command('help')
@bot.event
async def on_ready():
    return

@bot.event
async def on_message(message):
    return


bot.run(token)