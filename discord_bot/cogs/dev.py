import asyncio
import fileinput
from decouple import config
from discord.ext import commands


"""
Commands:
    -foo: obivious
    -reload: reloads a cog, used to update
             commands without closing the bot
    -gtfo: closes bot, in a rude way
    -delete: deletes given number of messages
    -authorize: authorize a user to use these commands

TODO
-Developer authorization
"""


class dev(commands.Cog, name="dev"):
    def __init__(self, bot):
        self.bot = bot
        self.AUTHORIZED_DEV_DC_ID = config("AUTHORIZED_DEV_DC_ID").split(",")

    async def cog_check(self, context):
        is_authorized = str(context.author.id) in self.AUTHORIZED_DEV_DC_ID
        if is_authorized:
            return is_authorized
        else:
            await context.message.reply("You are not authorized to use dev commands.")
            return is_authorized

    @commands.command(name="authorize")
    async def authorize(self, context, user_id: str):
        for line in fileinput.input(".env", inplace=True):
            if "AUTHORIZED_DEV_DC_ID" in line:
                self.AUTHORIZED_DEV_DC_ID.append(user_id)
                new_authorized = ",".join(self.AUTHORIZED_DEV_DC_ID)
                new_line = "AUTHORIZED_DEV_DC_ID=" + new_authorized
                print(new_line, end="\n")
            else:
                print(line, end="")

    @commands.command(
        name="foo", help="Replies to your foo-ish message in a foo-ish way"
    )
    async def foo(self, context):
        await context.message.reply("Foo indeed.")

    @commands.command(
        name="reload", aliases=["update"], help="Reloads (updates) given command(s)"
    )
    async def reload(self, context, *args):
        print("Reloading Cogs:")
        for cog in args:
            try:
                self.bot.reload_extension("cogs." + cog)
                print(f"\t-{cog} reloaded")
            except Exception as ex:
                print(f"\t-{cog} not reloaded\n\t\t{ex}")

    @commands.command(
        name="gtfo",
        aliases=["bye", "fuckoff", "poweroff", "close"],
        help="Closes the bot",
    )
    async def gtfo(self, context):
        print(f"Bot closed by {context.message.author}")
        await context.message.add_reaction("🖕")
        response = await context.message.reply("Alright dude, chill. I'm out.")
        await asyncio.sleep(3)
        await response.delete()
        await self.bot.logout()

    @commands.command(
        name="delete",
        aliases=["purge", "clear"],
        help="Deletes given number of previous messages (max. 100)",
    )
    async def delete(self, context, num_messages: int):
        channel = context.channel
        await channel.purge(limit=num_messages + 1, check=None, before=None)
        response = await channel.send(f"Deleted {num_messages} message(s)")
        await asyncio.sleep(3)
        await response.delete()


def setup(bot):
    bot.add_cog(dev(bot))
