import asyncio
import logging
import json

import discord
from discord.ext import commands

API = "https://servers-live.fivem.net/api/servers/"
IMAGE = "https://pbs.twimg.com/profile_images/847824193899167744/J1Teh4Di.jpg"

LOGGER = logging.getLogger("MEKAsystems")


class FiveM:
    def __init__(self, bot):
        self.bot = bot
        self.servers = []
        self.bot.loop.create_task(self.fetch_servers())

    @commands.is_owner()
    @commands.command()
    async def dumpservers(self, ctx):
        """
        Dumps the FiveM servers into a JSON file.
        """
        # Send a typing
        await ctx.trigger_typing()
        # Open fivem.json for writing
        with open("fivem.json", "w") as file:
            # And dump the list of servers
            json.dump(self.servers, file, sort_keys=True, indent=4)
        # Finally, notify the user about what we have done
        await ctx.send("Done! Check fivem.json for the dumped data.")

    @commands.command()
    async def fivem(self, ctx):
        """
        Shows general information about the FiveM servers.
        """
        # Send a typing
        await ctx.trigger_typing()
        # Create an embed
        embed = discord.Embed(title="FiveM Servers", colour=0xD89324)
        # Set the FiveM icon as the thumbnail
        embed.set_thumbnail(url=IMAGE)
        # Add the data
        embed.add_field(name="Number of Servers", value=len(self.servers), inline=False)
        # And send the embed
        await ctx.send(embed=embed)

    async def fetch_servers(self):
        """
        Gets the FiveM servers via the API.
        """
        # Wait until the bot is ready
        await self.bot.wait_until_ready()
        # While the bot is not closed
        while not self.bot.is_closed():
            # Get the servers from the API
            async with self.bot.http._session.get(API) as resp:
                # And store the servers
                self.servers = await resp.json()
            # Log that we have refreshed the FiveM Server list
            LOGGER.info("FiveM Server list has been updated")
            # Once is completed, wait 60 seconds until we try again
            await asyncio.sleep(60)


def setup(bot):
    bot.add_cog(FiveM(bot))
