import asyncio

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


@client.command(name='play', help='Play a game!')
async def _play(ctx, *, member: discord.Member):
    print('LOG: ' + str(ctx.author) + ' requested "Play"')
    player1 = ctx.author
    player1id = ctx.author.id
    yes = '👍'
    msg = await ctx.send('**Waiting for {0} to accept...**'.format(member))
    await msg.add_reaction(yes)

    def check(reaction, user):
        return user == member and str(reaction.emoji) in ['👍']

    loop = 0
    while loop == 0:
        try:
            reaction, user = await client.wait_for('reaction_add', check=check, timeout=10)
        except asyncio.TimeoutError:
            await ctx.send('**{0} didn\'t accept in time!**'.format(member))
            player1 = None
            loop = 1
        else:
            if reaction.emoji == yes:
                await ctx.send('**Accepted!**')
                player2 = member
                player2id = member.id
                await game(ctx, player1, player2, player1id, player2id)
                loop = 1


@_play.error
async def info_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        print('LOG: ' + str(ctx.author) + ' requested "Play", but it failed! (no arg)')
        await ctx.send('**To play a game, mention someone!** `rps!play @Friend`')


async def winning(ctx, player1, player2, p1r, p2r, p1p, p2p, p1s, p2s):
    if p1r and p2r or p1p and p2p or p1s and p2s:
        ctx.send('**It\'s a tie!**')
    if p1r and p2s or p1p and p2r or p1s and p2p:
        ctx.send('**' + player1 + ' won!**')
    else:
        ctx.send('**' + player2 + ' won!**')


async def game(ctx, player1, player2, player1id, player2id):
    user1 = client.get_user(player1id) # person who input command
    user2 = client.get_user(player2id) # person who accepted
    rock = '✊'
    paper = '✋'
    scissors = '✌'
    msg1 = await user1.send('Game with ' + str(player2) + '\nReact with your choice of Rock, Paper, or Scissors:')
    msg2 = await user2.send('Game with ' + str(player1) + '\nReact with your choice of Rock, Paper, or Scissors:')
    await msg1.add_reaction(rock)
    await msg2.add_reaction(rock)
    await msg1.add_reaction(paper)
    await msg2.add_reaction(paper)
    await msg1.add_reaction(scissors)
    await msg2.add_reaction(scissors)
    p1r = False
    p1p = False
    p1s = False
    p2r = False
    p2p = False
    p2s = False
    confirmed1 = False
    confirmed2 = False
    def check(reaction, user):
        return user == player1 and str(reaction.emoji) in ['✊', '✋', '✌']

    async def confirm1():
        await user1.send('Selected! ✅')
        confirmed1 = True

    async def confirm2():
        await user2.send('Selected! ✅')
        confirmed2 = True

    loop = 0
    while loop == 0:
        reaction, user = await client.wait_for('reaction_add', check=check)
        if reaction.emoji == rock:
            await confirm1()
            p1r = True
            loop = 1
        if reaction.emoji == paper:
            await confirm1()
            p1p = True
            loop = 1
        if reaction.emoji == scissors:
            await confirm1()
            p1s = True
            loop = 1

    def check(reaction, user):
        return user == player2 and str(reaction.emoji) in ['✊', '✋', '✌']

    loop = 0
    while loop == 0:
        reaction, user = await client.wait_for('reaction_add', check=check)
        if reaction.emoji == rock:
            await confirm2()
            p2r = True
            loop = 1
        if reaction.emoji == paper:
            await confirm2()
            p2p = True
            loop = 1
        if reaction.emoji == scissors:
            await confirm2()
            p2s = True
            loop = 1
    if confirmed1 and confirmed2:
        print('confirm test')
        await winning(ctx, player1, player2, p1r, p2r, p1p, p2p, p1s, p2s)


client.run(token)