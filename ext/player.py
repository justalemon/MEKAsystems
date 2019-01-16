import asyncio

import discord
import youtube_dl
from discord.ext import commands

YTDL_OPTS = {
    "format": "bestaudio/best",
    "outtmpl": "music/%(extractor)s/%(id)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0"
}
FFMPEG_OPTS = {
    "options": "-vn"
}
YTDL = youtube_dl.YoutubeDL(YTDL_OPTS)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        # Initialize the PCMVolumeTransformer with the source and volume
        super().__init__(source, volume)
        # Store the data, title and url
        self.data = data
        self.title = data.get("title")
        self.url = data.get("url")

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        # Get the event loop
        loop = loop or asyncio.get_event_loop()
        # Get the data of the video
        data = await loop.run_in_executor(None, lambda: YTDL.extract_info(url, download=not stream))

        # If is a playlist
        if "entries" in data:
            # Grab the first item
            data = data["entries"][0]

        # Use the URL if is a stream, otherwise prepare the download
        filename = data["url"] if stream else YTDL.prepare_filename(data)
        # Finally, return the new instance with the file and FFmpeg options
        return cls(discord.FFmpegPCMAudio(filename, **FFMPEG_OPTS), data=data)


class Player:
    def __init__(self, bot):
        self.bot = bot

    async def __local_check(self, ctx):
        # Only run the commands if we are in a guild (no PMs)
        return ctx.guild is not None

    @commands.command()
    async def play(self, ctx, *, url):
        """
        Plays the specified URL (it needs to be suported by YTDL).
        """
        # If there is no URL, return and notify the user
        if not url:
            await ctx.send("You have not specified an url.")
            return

        # Start typing
        async with ctx.typing():
            # Create a player with the user URL
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            # And play that
            ctx.voice_client.play(player)

        # Finally, send the current song playing
        await ctx.send(f"Now playing `{player.title}`")

    @commands.command()
    async def stream(self, ctx, *, url):
        """
        Plays a Stream of audio (it does not downloads the files).
        """
        # If there is no URL, return and notify the user
        if not url:
            await ctx.send("You have not specified an url.")
            return

        # Start typing
        async with ctx.typing():
            # Create a player from the loop
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            # And play that stream
            ctx.voice_client.play(player)

        # Finally, notify that we are playing the stream
        await ctx.send(f"Now playing `{player.title}`")

    @commands.command()
    async def join(self, ctx):
        """
        Joins the voice channel where the command author is.
        """
        # If the user has a voice state
        if ctx.author.voice:
            # Check if the bot is on a voice channel
            if ctx.voice_client:
                # If it does, move the bot
                await ctx.voice_client.move_to(ctx.author.voice.channel)
            else:
                # Otherwise, join the channel as usual
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

    @play.before_invoke
    @stream.before_invoke
    async def ensure_playback(self, ctx):
        """
        Function that makes sure that there is a channel available.
        """
        # If the bot is not connected to a voice channel
        if ctx.voice_client is None:
            # But the command author is connected to a voice channel
            if ctx.author.voice:
                # Connect to that voice channel
                await ctx.author.voice.channel.connect()
            else:
                # Otherwise, notify and return
                await ctx.send("You are not connected to a voice channel.")
        # Otherwise if the channel is playing
        elif ctx.voice_client.is_playing():
            # Stop the playback
            ctx.voice_client.stop()


def setup(bot):
    bot.add_cog(Player(bot))
