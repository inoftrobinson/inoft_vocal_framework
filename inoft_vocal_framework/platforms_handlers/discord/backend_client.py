# invite : https://discordapp.com/oauth2/authorize?client_id=713363868226945054&scope=bot&permissions=8
# token :

from discord.ext import commands
from discord.ext.commands.context import Context
from discord.message import Message
from inoft_vocal_engine.inoft_vocal_framework.platforms_handlers.discord import writing_func as wf
from inoft_vocal_engine.inoft_vocal_framework.platforms_handlers.discord import DiscordStaticInfos


bot_client = commands.Bot(command_prefix=DiscordStaticInfos.COMMAND_PREFIX)
# If you have the error CERTIFICATE_VERIFY_FAILED, you have an issue with a missing SSL certificate on your computer.
# Go to this link : https://crt.sh/?id=2835394 and click on "Download Certificate: PEM" at the bottom right of the page,
# it will download a SSL Certificate, that you must install. PS : The certificate is only valid until 2038 !

private_state = False
m_type = 'launch'

@bot_client.event
async def on_ready():
    print('Connected')

@bot_client.command()
async def ping(context: Context):
    await context.send(f'Pong! {round(bot_client.latency*1000)} ms')

@bot_client.command()
async def private(context: Context):
    # user grabbing by id
    user = bot_client.get_user(context.message.author.id)
    # dm sending by user (id)
    await user.send('Voulez vous parler dans un channel privé ou non ?')

@bot_client.command()
async def launch(context: Context):
    await wf.send_poll('Voulez vous jouer en textuel privé ou public ?', context, 'num', m_type, 2)

@bot_client.command()
async def testpoll(context: Context):
    await wf.send_poll("poll test", context, 'num', m_type, 5)
    print(context)

@bot_client.command()
async def testmess(context: Context):
    await wf.send_message(message_to_send="message test", destination_context=context)

@bot_client.event
async def on_reaction_add(reaction, user):
    author = reaction.message.author

    if user == author:
        return
    else:
        await wf.emojis_reaction_response(m_type, reaction, user)

@bot_client.event
async def on_message(message: Message):
    prefix_debug = message.content[:1]
    if message.author == bot_client.user:
        return
    elif message.content[:1] != DiscordStaticInfos.COMMAND_PREFIX:

        # user grabbing by id
        user = bot_client.get_user(message.author.id)
        from inoft_vocal_engine.inoft_vocal_framework.platforms_handlers.discord.handler_input import DiscordHandlerInput
        DiscordHandlerInput.HANDLER_FUNCTION_TO_USE(event=message, context=None)

        """
        print(f"Channel id beach {message.channel.id} & type : {type(message.channel.id)}")
        print(f"user id ea {message.author.id} & type : {type(message.author.id)}")
        print(f"Channel id beach {message.channel} & type : {type(message.channel)}")
        print(f"user id ea {message.author} & type : {type(message.author)}")

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
        """

    await bot_client.process_commands(message)
