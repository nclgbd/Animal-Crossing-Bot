import discord
import datetime
import json
import sys
import re
import random

from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import CommandNotFound
from scripts.FriendCodeHelper import *
from scripts.TurnipHelper import *

INFO = str(open('config/config.txt', 'r+').read()).split('\n')
TOKEN = INFO[0]
PREFIX = INFO[1]


client = commands.Bot(command_prefix = PREFIX)
start_time = datetime.datetime.utcnow()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print('------')
    await client.change_presence(activity=discord.Game(name='Animal Crossing New Horizons', type=1))


@client.command()
async def ping(ctx):
    await ctx.send('pong')
    

@client.command(name='uptime',
                description='Returns how long the bot has been running for.')
async def uptime(ctx):
    '''
    Source: https://stackoverflow.com/questions/52155265/my-uptime-function-isnt-able-to-go-beyond-24-hours-on-heroku
    '''
    now = datetime.datetime.utcnow() # Timestamp of when uptime function is run
    delta = now - start_time
    
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    
    if days:
        time_format = "**{d}** days, **{h}** hours, **{m}** minutes, and **{s}** seconds."
        
    else:
        time_format = "**{h}** hours, **{m}** minutes, and **{s}** seconds."
        
    uptime_stamp = time_format.format(d=days, h=hours, m=minutes, s=seconds)
    await ctx.send('{} has been up for {}'.format(client.user.name, uptime_stamp))
 

@client.command(name='info',
                description='Returns information about the bot',
                aliases=['botinfo', 'bot_info'])
async def bot_info(ctx):
    with open('media/isabelle_urls.json') as f:
        isabelle_urls = json.load(f)["isabelle_urls"]
        
    embed = discord.Embed(
        title='Animal Crossing Bot',
        description='Utility bot for Animal Crossing users'
    )
    
    embed.set_footer(text='You can view my code here: https://github.com/nguobadia/Animal-Crossing-Bot')
    embed.set_image(url=random.choice(isabelle_urls))
    
    await ctx.send(embed=embed)
 
 
'''FRIEND CODES'''

@client.command(name='add',
                description='Adds information to the database',
                aliases=['addfc'])
async def add_fc(ctx, *arg):
    ''' Currently adds user to friend code database.
    '''
    if arg[0] == 'fc' or arg[:2] == ('friend', 'code'):
        user_id = ctx.message.author.id
        if arg[:2] == ('friend', 'code'):
            ret = set_friend_code(user_id, arg[2])
        else:
            ret = set_friend_code(user_id, arg[1])
            
        if not ret:
            await ctx.send('Added {} successfully'.format(ctx.message.author))
        elif ret == -1:
            await ctx.send('Invalid friend code. Nintendo friend codes follow the pattern: SW-XXXX-XXXX-XXXX.')


@client.command(name='get',
                description='Gets information from the database',
                aliases=['getfc'])
async def get_fc(ctx, *arg):
    ''' Currently retrieves user's friend code from database.
    '''
    mentioned_user_id = ctx.message.mentions[0].id
    friend_code = get_friend_code(mentioned_user_id)
    
    if friend_code == -1:
        await ctx.send('User not found.')
    else:
        await ctx.send(friend_code)




''' TURNIPS '''
@client.command(name='turnip',
                description='Retrieves the turnip prophet link.')
async def turnip(ctx, *arg):
    if arg[0] == 'prophet' or arg[0] == 'link':
        await ctx.send(get_turnip_profit_link())



client.run(TOKEN)