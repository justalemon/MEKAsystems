import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")

    @commands.command()
    async def help(self, ctx, *, uinput=None):
        """Shows this help command."""
        # Create a place to store the commands
        coms = []

        # Iterate over the current commands
        for com in self.bot.commands:
            # Check if the user can use the command
            try:
                await com.can_run(ctx)
            # If there was a check error, skip it
            except commands.CommandError:
                pass
            # Otherwise, add it on the list
            else:
                coms.append(com)

        # Sort the commands by their name
        coms = sorted(coms, key=lambda command: command.name)

        # Create a place to store our page index
        index = 0
        # If the user entered a value
        if uinput:
            # And is numeric
            if uinput.isnumeric():
                # Set that as index
                index = int(uinput) - 1

        # Store the index for the first and last command to show
        first = 5 * index
        last = 5 * index + 5
        # If the first element is higher than the available commands
        if first >= len(coms):
            # Notify the user that the help page is invalid and return
            await ctx.send("Looks like this help page is invalid.")
            return
        # If the last element is higher than the available commands
        if last > len(coms):
            # Just show until the last command
            last = len(coms)

        # Replace the list of commands with the ones that we have
        coms = coms[first:last]

        # Create an embed to show the commands
        embed = discord.Embed(title="{0} commands".format(ctx.me.name), colour=0x7FD935)
        # Sets the Bot avatar as the thumbnail
        embed.set_thumbnail(url=ctx.me.avatar_url)
        # For each command in the list of commands
        for command in coms:
            # Add a field with the command and the description of it
            embed.add_field(name=self.bot.command_prefix + command.name,
                            value=command.help.splitlines()[0], inline=False)
        # Finally, send the embed with the available commands for the user
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
