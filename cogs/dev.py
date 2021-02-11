import discord
from discord.ext import commands


class dev(commands.Cog, name='dev'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='foo',
                      help='Replies to your foo-ish message in a foo-ish way')
    async def foo(self, context):
        await context.message.reply('Foo indeed.')

    @commands.command(name='reload',
                      aliases=['update'],
                      help='Reloads (updates) given command(s)')
    async def reload(self, context, *args):
        print('Reloading Cogs:')
        for cog in args:
            try:
                self.bot.reload_extension('cogs.' + cog)
                print(f'\t-{cog} reloaded')
            except Exception as ex:
                print(f'\t-{cog} not reloaded\n\t\t{ex}')
                
    @commands.command(name='gtfo',
                      aliases=['bye', 'fuckoff', 'poweroff', 'close'],
                      help='Closes the bot')
    async def gtfo(self, context):
        print(f'Bot closed by {context.message.author}')
        await context.message.add_reaction('🖕')
        await context.message.reply('Alright dude, chill. I\'m out.')
        await self.bot.logout()

def setup(bot):
    bot.add_cog(dev(bot)) 