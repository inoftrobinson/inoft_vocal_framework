import discord
#from discord.ext import commands


def emoji_array(e_type, number):
    numeric_emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
    behavior_emojis = []

    if e_type == 'num':
        tab = numeric_emojis[0:number]
    elif e_type == 'behav':
        tab = behavior_emojis[0:number]

    return tab


# general function to send polls
async def send_poll(message_to_send, destination, e_type, m_type, number):
    message = await destination.send(message_to_send)
    reactions = emoji_array(e_type, number)
    for emoji in reactions:
        await message.add_reaction(emoji)

# general function to send messages
async def send_message(message_to_send, destination):
    await destination.send(message_to_send)

# function with all response options to aa reaction add
async def emojis_reaction_response(m_type, reaction, user):
    if m_type == 'launch':
        if reaction.emoji == '1️⃣':
            await user.send('Continuons ici !')
            reaction.message.delete()
        elif reaction.emoji == '2️⃣':
            await reaction.message.channel.send('Continuons ici !')
            reaction.message.delete()
        else:
            await reaction.message.channel.send('Reaction innapropriée')
    elif m_type == 'game':
        return m_type
