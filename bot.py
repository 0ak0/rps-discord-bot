import discord
import os
import time
from discord.ext import commands
from discord.ext.commands import has_permissions
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix='rps!')

# How a normal, single playthrough should work:
# Player A runs 'rps!play' and tags Player B
# Player B responds (most likely by reaction)
# Both players are DM'ed and choose Rock, Paper, or Scissors
# Once both answers are in, choose winner (R>S, P>R, S>P)


@client.event
async def on_ready():
    print(f'{client.user} connected.')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="rps!play"))


@client.command(help='Play a game!')
async def play(ctx):
    print('LOG: ' + str(ctx.author) + ' requested "Play"')
    await ctx.send('test')

client.run(token)