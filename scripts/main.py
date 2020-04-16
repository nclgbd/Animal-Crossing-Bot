import discord
import datetime
import json
import sys
import re

from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import CommandNotFound

INFO = str(open('config/config.txt', 'r+').read()).split('\n')
TOKEN = INFO[0]
PREFIX = INFO[1]
FRIEND_CODE_PATH = 'config/friend_codes.json'

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
 
@client.command(name='add',
                description='Adds information to the database')
async def add(ctx, *arg):
    ''' Currently adds user to friend code database.
    '''
    if arg[:2] == ('friend', 'code'):
        user_id = ctx.message.author.id
        ret = set_friend_code(user_id, arg[2])
        if not ret:
            await ctx.send('Added {} successfully'.format(ctx.message.author))
            
        elif ret == -1:
            await ctx.send('Invalid friend code. Nintendo friend codes follow the patter SW-XXXX-XXXX-XXXX.')

@client.command(name='get',
                description='Gets information from the database')
async def get(ctx, *arg):
    ''' Currently retrieves user's friend code from database.
    '''
    if arg[:2] == ('friend', 'code'):
        mentioned_user_id = ctx.message.mentions[0].id
        friend_code = get_friend_code(mentioned_user_id)
        await ctx.send(friend_code)



''' set commands'''
def set_friend_code(user_id, friend_code):
    regex = 'SW-[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]'
    if re.findall(regex, friend_code):
        user_and_code = {
            user_id: friend_code
        }
    
        with open(FRIEND_CODE_PATH, 'w+') as wf:
            json.dump(user_and_code, wf)
            return 0
        
    else:
        return -1
        
    
    
''' get commands'''
def get_friend_code(user_id):
    return load_friend_codes(user_id)
    
def load_friend_codes(user_id):
    with open(FRIEND_CODE_PATH) as f:
        friend_codes = json.load(f)
    
    return friend_codes[str(user_id)]
    
client.run(TOKEN)