# invite : https://discordapp.com/oauth2/authorize?client_id=713363868226945054&scope=bot&permissions=8
# token : NzEzMzYzODY4MjI2OTQ1MDU0.XsfB5A.kVzkMJfcEWPBUumQ7bHS4s_lZKQ
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

@client.command()
async def private(ctx):
    #user grabbing by id
    user = client.get_user(ctx.message.author.id)
    #dm sending by author method
    await ctx.author.send('Voulez vous parler dans un channel privé ou non ?')
    #dm sending by user (id)
    await user.send('Voulez vous parler dans un channel privé ou non ?')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif message.content[:1] != prfx:

        #user grabbing by id
        user = client.get_user(message.author.id)

        data = {
            'author_name':message.author.name,
            'author_id':message.author.id,
            'message':message.content,
            'time':message.created_at
        }

        print(data)

        #public channel sending 
        await message.channel.send(data)
        #sending private response to the last person sending a message
        await message.author.send(data)
        #sending private response to a spécific person whom we grabbed his id before
        await user.send(data)


    await client.process_commands(message)

client.run('NzEzMzYzODY4MjI2OTQ1MDU0.XsfB5A.kVzkMJfcEWPBUumQ7bHS4s_lZKQ')
