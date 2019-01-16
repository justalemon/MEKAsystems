from discord.ext import commands


class Player:
    def __init__(self, bot):
        self.bot = bot

    async def __local_check(self, ctx):
        # Only run the commands if we are in a guild (no PMs)
        return ctx.guild is not None

    @commands.command()
    async def join(self, ctx):
        """
        Joins the voice channel where the command author is.
        """
        # If the user has a voice state
        if ctx.author.voice:
            # Join the user channel
            await ctx.author.voice.channel.connect()
        # Otherwise, notify the user
        else:
            await ctx.send("You are not using a voice channel.")

    @commands.command()
    async def leave(self, ctx):
        """
        Leaves the current voice channel.
        """
        # If there is a voice channel, leave it
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
        # Otherwise, notify the user that there is no voice channel
        else:
            await ctx.send("The bot is not connected to a voice channel.")


def setup(bot):
    bot.add_cog(Player(bot))
