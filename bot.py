import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from keep_alive import keep_alive
from collections import Counter
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
keep_alive()
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
pemis_count = {}
last = 0
pemis_id = 1394948705647464491
explain_message = """Pemis is a meme in the Lofers Community that originated from [here](https://discord.com/channels/1378361814672216144/1383767207049171005/1390991554956492800)."""
commands_list = """- `.pemiscount <user (optional)>`: displays the number of times you (or the specified user) have said "pemis", along with their rank on the server.
- `.leaderboard <num (optional)>`: Shows the server leaderboard of the top users based on "pemis" count. If no number is provided, it defaults to showing the top 10."""
def get_rank(id):
    c = Counter(pemis_count)
    cs = c.most_common()
    rank = cs.index((id, pemis_count[id]))
    return rank


bot = commands.Bot(command_prefix='.', intents=intents)
bot.remove_command('help')
@bot.event
async def on_ready():
    print("The bot is online.")

@bot.event
async def on_message(message):
    global last
    if message.channel.id==pemis_id:
        if message.content.lower() == "pemis" and message.author.id != last:
            await message.add_reaction("⛓️")
            last = message.author.id
            if str(message.author.id) in pemis_count.keys():
                pemis_count[str(message.author.id)] += 1
            else:
                pemis_count[str(message.author.id)] = 1
        elif message.content[:3] == "-# ":
            return
        else:
            await message.delete()
    await bot.process_commands(message)

@bot.command()
async def pemiscount(ctx, user: discord.User = None):
    if user != None:
        if str(user.id) in pemis_count.keys():
            count = pemis_count[str(user.id)]
            color = random.randint(0x000000,0xFFFFFF)
            embedVar = discord.Embed(color=color)
            embedVar.add_field(name="Pemis count", value=f'<@{str(user.id)}> has said "Pemis" {count} times', inline=False)
            embedVar.add_field(name="Rank", value=f'Their position in the server is: {get_rank(str(user.id))+1}', inline=False)
            await ctx.reply(embed=embedVar)
        else:
            color = random.randint(0x000000, 0xFFFFFF)
            embedVar = discord.Embed(color=color)
            embedVar.add_field(name="Pemis count", value=f'<@{str(user.id)}> has never said "Pemis"', inline=False)
            await ctx.reply(embed=embedVar)
    else:
        if str(ctx.author.id) in pemis_count.keys():
            count = pemis_count[str(ctx.author.id)]
            color = random.randint(0x000000,0xFFFFFF)
            embedVar = discord.Embed(color=color)
            embedVar.add_field(name="Pemis count", value=f'You have said "Pemis" {count} times', inline=False)
            embedVar.add_field(name="Rank", value=f'Your position in the server is: {get_rank(str(ctx.author.id))+1}', inline=False)
            await ctx.reply(embed=embedVar)
        else:
            color = random.randint(0x000000, 0xFFFFFF)
            embedVar = discord.Embed(color=color)
            embedVar.add_field(name="Pemis count", value=f'You have never said "Pemis"', inline=False)
            await ctx.reply(embed=embedVar)

@bot.command()
async def leaderboard(ctx, num = 10):
    num = int(num)
    if len(pemis_count.items()) < num:
        await ctx.reply("There are too few people in the leaderboard. Try with a smaller number.")
    else:
        c = Counter(pemis_count)
        cs = c.most_common(num)
        leaderboard_text = ""

        for index, item in enumerate(cs):
            leaderboard_text += f'{index}. <@{item[0]}>: {item[1]}\n'

        color = random.randint(0x000000, 0xFFFFFF)
        embedVar = discord.Embed(color=color)
        embedVar.add_field(name=f"Top {num} leaderboard", value=leaderboard_text, inline=False)
        await ctx.reply(embed=embedVar)

@bot.command()
async def help(ctx):
    embedVar = discord.Embed(title="Pemis Bot", color=0x00FF00)
    embedVar.add_field(name="What's Pemis?", value=explain_message, inline=False)
    embedVar.add_field(name="Commands", value=commands_list, inline=False)
    await ctx.reply(embed=embedVar)

@bot.command()
async def reevaluate(ctx):
    if ctx.author.id == 732244359193559091:
        global pemis_count
        pemis_count = {}
        channel = bot.get_channel(pemis_id)
        async for message in channel.history():
            if message.content.lower() == "pemis":
                if str(message.author.id) in pemis_count.keys():
                    pemis_count[str(message.author.id)] += 1
                else:
                    pemis_count[str(message.author.id)] = 1
        embedVar = discord.Embed(color=0x00FF00)
        embedVar.add_field(name="", value=f"Reevaluated. This is the current list:\n{pemis_count}")
        await ctx.reply(embed=embedVar)
bot.run(token)