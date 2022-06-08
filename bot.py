import os
import random

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

@bot.command(name='poro', help='Talk with Poro :)')
async def poro(ctx):
    poro_quotes = [
        'Tengo hambre...',
        'Grrrr!',
        (
            'Es hora de League of Legends! '
            "Let's go"
        ),
        'Dame amor <3',
        'Cookies!',
        ':3'
    ]

    response = random.choice(poro_quotes)
    await ctx.send(response)

@bot.command(name='decide', help='Poro decides for you.')
async def decide(ctx, *options: str):
    decision = options[random.choice(range(0, len(options)))]
    await ctx.send("Poro ha decidido que lo mejor es: " + decision)

bot.run(TOKEN)