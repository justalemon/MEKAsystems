import logging

import discord
from discord.ext import commands
from motor.motor_asyncio import AsyncIOMotorClient

INVITE = "https://discordapp.com/oauth2/authorize?client_id={0}&scope=bot&permissions=104066247"

logger = logging.getLogger("MEKAsystems")


class MEKAsystems(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        # If there is a MongoDB URL on the keyword arguments
        if kwargs.get("mongourl"):
            # Create an instance of the MongoDB Asyncio client
            logger.info("MongoDB URL found, attempting connection...")
            self.db = AsyncIOMotorClient(kwargs.get("mongourl"))
            # And remove the keyword argument
            kwargs.pop("mongourl")
        # If there is no MongoDB URL
        else:
            # Set it as None
            self.db = None

        # Initialize a normal Auto Sharded Bot
        super().__init__(*args, **kwargs)
        # Remove the default help command
        self.remove_command("help")
        # And add the stop and new help commands
        self.add_command(self.stop)
        self.add_command(self.invite)
        self.add_command(self.help)

    async def on_command(self, ctx):
        """Notify the Bot Owner when someone executes a command."""
        logger.info("Command by {0.name} ({0.id}): {1.content}".format(ctx.author, ctx.message))

    async def on_ready(self):
        """Notify the Bot Owner when we are ready to work."""
        info = await self.application_info()
        logger.info(f"Ready to work! The prefix is '{self.command_prefix}' and ID is '{info.id}'")
        # Change the presence to the help command
        game = discord.Game("{0}help".format(self.command_prefix))
        await self.change_presence(activity=game)

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
        info = await self.application_info()
        # And return the invite with the client id
        await ctx.send(INVITE.format(info.id))

    @commands.command()
    async def help(self, ctx, *, uinput=None):
        """Shows this help command."""
        # Create a place to store the commands
        coms = []

        # Iterate over the current commands
        for com in self.commands:
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
            embed.add_field(name=self.command_prefix + command.name,
                            value=command.help.splitlines()[0], inline=False)
        # Finally, send the embed with the available commands for the user
        await ctx.send(embed=embed)
