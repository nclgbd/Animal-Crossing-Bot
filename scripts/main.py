import discord
import datetime
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import CommandNotFound

INFO = str(open('configconfig.txt', 'r+').read()).split('\n')
TOKEN = INFO[0]
PREFIX = INFO[1]

client = commands.Bot(command_prefix = PREFIX)
start_time = datetime.datetime.utcnow()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print('------')
    await client.change_presence(activity=discord.Game(name='!help for bot info', type=1))

@bot.command()
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
    
client.run(TOKEN)

client.run('token')