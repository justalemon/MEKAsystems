from discord.ext import commands

INVITE = "https://discordapp.com/oauth2/authorize?client_id={0}&scope=bot&permissions=104066247"


class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def stop(self, ctx):
        """Stops the Bot safely."""
        await ctx.send("Bye!")
        await self.logout()

    @commands.command()
    async def invite(self, ctx):
        """
        Shows an invite link for the Bot.
        """
        # Get the application info
        info = await self.bot.application_info()
        # And return the invite with the client id
        await ctx.send(INVITE.format(info.id))


def setup(bot):
    bot.add_cog(Base(bot))
