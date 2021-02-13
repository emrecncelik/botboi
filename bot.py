import discord
import logging

from decouple import config
from tabulate import tabulate
from discord.ext import commands
from discord.ext.commands import Bot

# logging.basicConfig(level=logging.INFO)

PRFX = config('PRFX')
COGS = config('COGS').split(',')
DISCORD_API_TOKEN = config('DISCORD_API_TOKEN')

bot = Bot(command_prefix=PRFX)


@bot.event
async def on_ready():
    active_guilds = [(guild.name, guild.member_count) for guild in bot.guilds]
    active_guilds = tabulate(active_guilds,
                             headers=['Name', 'Member Count'],
                             tablefmt='orgtbl')
    print(f'Logged in as {bot.user}')
    print(f'Active guilds:\n{active_guilds}\n')
    print(f'Loading Cogs:')

    # Automatically load cogs on start
    for cog in COGS:
        try:
            bot.load_extension('cogs.' + cog)
            print(f'\t-{cog} loaded')
        except Exception as ex:
            print(f'\t-{cog} not loaded\n\t\t{ex}')


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    

bot.run(DISCORD_API_TOKEN)