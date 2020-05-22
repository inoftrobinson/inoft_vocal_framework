# invite : https://discordapp.com/oauth2/authorize?client_id=713363868226945054&scope=bot&permissions=8
# token :

import discord
from discord.ext import commands

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print('Connected')



@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency*1000)} ms')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    #if something intersting:
        #process
        #await message.channel.send(reponse)
    await client.process_commands(message)

client.run('')
