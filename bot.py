import logging

import discord
from discord.ext import commands
from motor.motor_asyncio import AsyncIOMotorClient

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
