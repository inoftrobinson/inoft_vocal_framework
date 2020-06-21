# invite : https://discordapp.com/oauth2/authorize?client_id=713363868226945054&scope=bot&permissions=8
# token : 
import json
import discord
import time
from discord.ext import commands
from discord.ext.commands.context import Context
from discord.message import Message
from discord.utils import get
from inoft_vocal_framework.platforms_handlers.discord import writing_func as wf


prfx = '.'
client = commands.Bot(command_prefix=prfx)
private_state = False
m_type = 'launch'


@client.event
async def on_ready():
    print('Connected')

@client.command()
async def ping(context: Context):
    await context.send(f'Pong! {round(client.latency*1000)} ms')

@client.command()
async def private(context: Context):
    #user grabbing by id
    user = client.get_user(context.message.author.id)
    #dm sending by user (id)
    await user.send('Voulez vous parler dans un channel privé ou non ?')

@client.command()
async def launch(context: Context):
    await wf.send_poll('Voulez vous jouer en textuel privé ou public ?', context, 'num', m_type, 2)

@client.command()
async def testpoll(context: Context):
    await wf.send_poll("poll test", context, 'num', m_type, 5)
    
    print(ctx)

@client.command()
async def testmess(context: Context):
    await wf.send_message("message test", context)

@client.event
async def on_reaction_add(reaction, user):
    author = reaction.message.author

    if user == author:
        return
    else:
        await wf.emojis_reaction_response(m_type, reaction, user)

@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return
    elif message.content[:1] != prfx:

        # user grabbing by id
        user = client.get_user(message.author.id)

        data = {
            "author_name": message.author.name,
            "author_id": message.author.id,
            "message": message.content,
            "time": message.created_at
        }

        print(data)

        # public channel sending
        await message.channel.send(data)
        # sending private response to a spécific person whom we grabbed his id before
        await user.send(data)


    await client.process_commands(message)

client.run('NzEzMzYzODY4MjI2OTQ1MDU0.XsrlzQ.tJ_-8rBh430Hzys_WvX6YGMZfco')
