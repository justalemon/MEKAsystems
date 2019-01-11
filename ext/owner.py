from discord.ext import commands


class Owner:
    def __init__(self, bot):
        self.bot = bot

    async def __local_check(self, ctx):
        # Make this cog commands only available for the Bot Owner
        return await self.bot.is_owner(ctx.author)

    @commands.command()
    async def setpic(self, ctx):
        """Sets the Bot picture from an attached image."""
        # Send a typing status
        await ctx.trigger_typing()
        # If there is no file attached
        if not len(ctx.message.attachments):
            # Notify the user and return
            await ctx.send("You have not uploaded an image.")
            return

        # Get the first attachment with aiohttp
        async with self.bot.http._session.get(ctx.message.attachments[0].url) as resp:
            # And set it as the profile picture
            await self.bot.user.edit(avatar=await resp.read())
        # And notify the user about it
        await ctx.send("Done!")


def setup(bot):
    bot.add_cog(Owner(bot))
