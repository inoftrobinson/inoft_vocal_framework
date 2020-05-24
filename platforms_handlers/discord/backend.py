# invite : https://discordapp.com/oauth2/authorize?client_id=713363868226945054&scope=bot&permissions=8
# token :
import json
import discord
from discord.ext import commands

prfx = '.'
client = commands.Bot(command_prefix = prfx)

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
    elif message.content[:1] != prfx:
        data = {
            'author_name':message.author.name,
            'author_id':message.author.id,
            'message':message.content,
            'time':message.created_at
        }
        print(data)
        await message.channel.send(data)
        
    await client.process_commands(message)

client.run('')
