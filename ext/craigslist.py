import re
import logging
from datetime import datetime

import discord
from aiohttp import ContentTypeError
from lxml import html

URL_REGEX = "https:\/\/[a-z]*.craigslist.org\/[a-z/]*\/d\/[a-z\-0-9]*\/[0-9]*.html"  # noqa: W605
DATE_IN = "%Y-%m-%dT%H:%M:%S%z"
DATE_OUT = "%B %d, %Y %I:%M %p"
XPATH_TITLE = "//span[@id='titletextonly']/text()"
XPATH_IMAGE = "//div[@class='slide first visible']//img[1]/@src"
XPATH_LOC = "//span[@class='postingtitletext']//small[1]/text()"
XPATH_TIME = "//div[@class='postinginfos']//time[@class='date timeago']/@datetime"
XPATH_TEXT = "//section[@id='postingbody']/text()"

LOGGER = logging.getLogger("MEKAsystems")


class Craigslist:
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message: discord.Message):
        """
        Checks if the message contains a Craigslist link and shows the information of it.
        """

        # Create the re thingy
        compiled = re.compile(URL_REGEX)
        # See if there is a match
        match = compiled.match(message.content)
        # If there is no matches, just return
        if not match:
            return

        # Get the Craigslist URL contents for parsing
        async with self.bot.http._session.get(match.group()) as resp:
            # And try to make lxml load the content
            try:
                parser = html.fromstring(await resp.text())
            except ContentTypeError:
                LOGGER.error(f"Unable to get '{match.group()}'")

        # Format the values correctly
        desc = "\n".join([x.replace("\n", "") for x in parser.xpath(XPATH_TEXT)])
        posted = datetime.strptime(parser.xpath(XPATH_TIME)[0], DATE_IN)
        # updated = datetime.strptime(parser.xpath(XPATH_TIME)[1], DATE_IN)
        # Create an embed to show the product information
        embed = discord.Embed(title=f"Craigslist: {parser.xpath(XPATH_TITLE)[0]}",
                              colour=0xFFFFFF, url=match.group(),
                              description=desc)
        embed.set_thumbnail(url=parser.xpath(XPATH_IMAGE)[0])
        embed.add_field(name="Location", value=re.sub("[()]", "", parser.xpath(XPATH_LOC)[0]))
        embed.add_field(name="Posted", value=posted.strftime(DATE_OUT))
        # embed.add_field(name="Updated", value=updated.strftime(DATE_OUT))
        # Finally, send the embed
        await message.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Craigslist(bot))
