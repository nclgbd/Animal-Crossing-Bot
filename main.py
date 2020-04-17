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


@client.command(name='ping',
                description='pong')
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
    
    ![add|addfc] [friend code|fc] @User
    
    Note: if you use !addfc then there's no need to include 'friend code' or 'fc'
    
    Examples:
        !add fc @Chonnasorn
        !addfc @Chonnasorn
        !add friend code @Chonnasorn
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
    
    ![get|getfc] [friend code|fc] @User
    
    Note: if you use !getfc then there's no need to include 'friend code' or 'fc'
    
    Examples:
        !get fc @Chonnasorn
        !getfc @Chonnasorn
        !get friend code @Chonnasorn
    '''
    mentioned_user_id = ctx.message.mentions[0].id
    friend_code = get_friend_code(mentioned_user_id)
    
    if friend_code == -1:
        await ctx.send('User not found.')
    else:
        await ctx.send(friend_code)



''' TURNIPS '''
@client.command(name='turnip',
                description='Turnip commands.')
async def turnip(ctx, *arg):
    ''' Used to calculate turnip price trends. The two websites used are https://turnipprophet.io/ and https://ac-turnip.com/. To use this command:
    !turnip [prophet|ac-turnip] [-b] p1 p2 p3 ... pn
    
    prophet: brings you to https://turnipprophet.io/ 
    ac-turnip: brings you to https://ac-turnip.com/ 
    -b: flag showing whether or not you're including the buying price. if not, ignore the flag
    p1 p2 ... pn: prices going Monday AM, Monday PM, ..., Saturday PM. entering a price of 0 indicates that you missed that day.
    
    Examples:
        !turnip prophet -b 101 78 94 65 0 44 
        !turnip ac-turnip 87 65 107 113 120 119 110 90
        !turnip prophet 0 0 0 0 90 0 56
    '''
    is_buying_price = arg[1] == '-b'
    try:
        if not is_buying_price:
            int(arg[1])
            
    except ValueError:
        pass
        
    else:
        link = ''
        cmd = arg[0]
        
        if is_buying_price:
            arg = [int(i) for i in arg[2:]]
        else:
            arg = [int(i) for i in arg[1:]]
            
             
        if cmd == 'prophet':
            link = generate_turnip_prophet_link(arg, is_buying_price)  
        elif cmd == 'ac-turnip':
            link = generate_turnip_ac_turnip_link(arg, is_buying_price)
        if link:
            await ctx.send(link)
        

client.run(TOKEN)