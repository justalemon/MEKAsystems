import asyncio
import logging
import json
import re

import discord
from aiohttp import ContentTypeError
from fuzzywuzzy import fuzz
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
    async def serverinfo(self, ctx, *, query=None):
        """
        Searches a FiveM server and show it's info.
        """
        # If there is no server selected, return
        if not query:
            await ctx.send("We need a text to search.")
            return
        # Get the servers in the format (Server, Ratio)
        output = [(x, fuzz.partial_ratio(x["Data"]["hostname"].encode("utf-8"), query))
                  for x in self.servers]
        # Order them by ratio
        output = sorted(output, key=lambda server: server[1], reverse=True)
        # If none of the matches are higher than 65 percent, return
        if not [x for x in output if x[1] > 65]:
            await ctx.send("No servers found.")
            return
        # Store the server data
        data = output[0][0]["Data"]
        # Use regex to remove the FiveM color tags
        title = re.sub(r"\^[0-9]", "", data["hostname"])
        # Create an embed to show the info
        embed = discord.Embed(title="FiveM Server Information", colour=0xD89324)
        # Calculate how many players are available
        players = "{0}/{1} ({2} available)".format(data["clients"], data["svMaxclients"],
                                                   data["svMaxclients"] - data["clients"])
        # Add the data
        embed.add_field(name="Server Name", value=title, inline=False)
        embed.add_field(name="Players", value=players)
        embed.add_field(name="Gamemode", value=data["gametype"])
        embed.add_field(name="Map", value=data["mapname"])
        embed.add_field(name="Resources", value=len(data["resources"]))
        embed.add_field(name="OneSync Enabled", value=data["vars"]["onesync_enabled"])
        embed.add_field(name="Server IP", value=output[0][0]["EndPoint"])
        # Finally, send the info
        await ctx.send(embed=embed)

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
                # And try store the servers
                try:
                    self.servers = await resp.json()
                except ContentTypeError:
                    LOGGER.error("Unable to get the FiveM Servers. Maybe the JSON is not valid?")
            # Log that we have refreshed the FiveM Server list
            LOGGER.info("FiveM Server list has been updated")
            # Once is completed, wait 60 seconds until we try again
            await asyncio.sleep(60)


def setup(bot):
    bot.add_cog(FiveM(bot))
