import io

import discord
from discord.ext import commands


class Admin:
    def __init__(self, bot):
        self.bot = bot

    async def __local_check(self, ctx):
        # Make this cog commands only available for administrators
        return ctx.channel.permissions_for(ctx.author).administrator

    @commands.command()
    async def purge(self, ctx, numberof=5):
        """
        Purges the specified number of commands.
        """
        await ctx.channel.purge(limit=numberof)
        await ctx.send("Purge finished!")

    @commands.command()
    async def roles(self, ctx, *, ftype="block"):
        """
        Shows the list of roles on the server.

        You can set the mode to receive the list of roles:

        1. block: Shows on a codeblock (not valid if the message size is higher than 2000)
        2. file: Returns a file with the list of roles
        """
        # Create a place to store the readable role format
        data = ""

        # For each role in the current guild roles
        for role in ctx.guild.roles:
            # If is not @everyone
            if role.name != "@everyone":
                # Add it in the format "ID: Name"
                data += "{0.id}: {0.name}\n".format(role)

        # If the length is higher than 2000 or the requested type is file
        if len(data) > 2000 or ftype == "file":
            # Create a file from the readable roles
            bio = io.BytesIO(bytes(data.encode("utf-8")))
            # And send the file
            await ctx.send(file=discord.File(bio, "roles.txt"))
        # Otherwise if the type is embed
        elif ftype == "block":
            # Send the data on a codeblock
            await ctx.send("```py\n" + data + "```")


def setup(bot):
    bot.add_cog(Admin(bot))
