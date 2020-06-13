# invite : https://discordapp.com/oauth2/authorize?client_id=713363868226945054&scope=bot&permissions=8
# token : 
import json
import discord
from discord.ext import commands


prfx = '.'
client = commands.Bot(command_prefix = prfx)
private_state = False


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
    #dm sending by user (id)
    await user.send('Voulez vous parler dans un channel privé ou non ?')

@client.command()
async def launch(ctx):
    message = await ctx.send('Voulez vous jouer en textuel privé ou public ?')
    for emoji in ('1️⃣', '2️⃣'):
        await message.add_reaction(emoji)
        #res = await ctx.wait_for_reaction()

@client.event
async def on_reaction_add(reaction, user):
    channel = reaction.message.channel
    message = reaction.message
    if user == client.user:
        return
    else:
        if reaction.emoji == '1️⃣':
            #delete last message and continue in private
            await message.delete()
            await user.send("Nous continuerons ici alors.")
            private_state = True
        elif reaction.emoji == '2️⃣':
            #delete last message and continue in the current channel
            await message.delete()
            await channel.send("Nous continuerons ici alors.")
        else:
            await channel.send("Réagissez avec une des réactions proposées")
        

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
        #sending private response to a spécific person whom we grabbed his id before
        await user.send(data)


    await client.process_commands(message)

client.run('')
