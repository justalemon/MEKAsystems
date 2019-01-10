import io

import discord
from discord.ext import commands


class Admin:
    def __init__(self, bot):
        self.bot = bot

    async def __local_check(self, ctx):
        return ctx.channel.permissions_for(ctx.author).administrator

    @commands.command()
    async def roles(self, ctx, *, ftype="embed"):
        """
        Shows the list of roles on the server.

        You can set the mode to receive the list of roles:

        1. embed: Shows on an embed (not valid if the message size is higher than 2000)
        2. file: Returns a file with the list of roles
        """
        data = ""

        for role in ctx.guild.roles:
            if role.name != "@everyone":
                data += "{0.id}: {0.name}\n".format(role)

        if len(data) > 2000 or ftype == "file":
            bio = io.BytesIO(bytes(data.encode("utf-8")))
            await ctx.send(file=discord.File(bio, "roles.txt"))
        elif ftype == "embed":
            await ctx.send("```py\n" + data + "```")


def setup(bot):
    bot.add_cog(Admin(bot))
