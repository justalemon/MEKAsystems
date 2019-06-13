import discord
from bot import MEKAsystems
from discord.ext import commands

CREATED = "\n\nCreated by [{0[login]}]({0[html_url]}) at {1}"
CLOSED = "\nClosed by [{0[login]}]({0[html_url]}) at {1}"
MERGED = "\nMerged by [{0[login]}]({0[html_url]}) at {1}"
PR = "\n\nCommits: {0[commits]}\nAdditions/Deletions: {0[additions]}/{0[deletions]}\nChanged Files: {0[changed_files]}"
OPEN = "\nThe issue is **open**"


class GitHub(commands.Cog):
    def __init__(self, bot):
        self.bot: MEKAsystems = bot

    @commands.command()
    async def issue(self, ctx: commands.Context, user: str, repo: str, number: str):
        """
        Gets the information of a GitHub issue or pull request.
        """
        # Generate the URL for the issue
        url: str = f"https://api.github.com/repos/{user}/{repo}/issues/{number}"

        # Use the existing bot session
        async with self.bot.session.get(url) as resp:
            # If the response was not 200
            if resp.status != 200:
                # Return with an error message
                await ctx.send("We didn't found that issue! Check that the the user, repo and number match.")
                return
            # Get the response as JSON
            json: dict = await resp.json()

        # Create an embed
        embed = discord.Embed()
        # Set the data of the embed
        embed.url = json["html_url"]
        embed.title = json["title"]
        embed.description = json["body"]
        embed.set_thumbnail(url=json["user"]["avatar_url"])

        # If this is a pull request
        if "pull_request" in json:
            # Get the pull request information
            async with self.bot.session.get(json["pull_request"]["url"]) as resp:
                # If the response was not 200
                if resp.status != 200:
                    # Add that the information is not complete
                    embed.description += "\n**Warning**: The information is not complete"
                # Get the response as JSON
                pr: dict = await resp.json()

            # Add the pull request information
            embed.description += PR.format(pr)

        # Add the creator information
        embed.description += CREATED.format(json["user"], json["created_at"])

        # If the issue is closed
        if json["state"] == "closed":
            # If this is a pull request
            if "pull_request" in json:
                embed.description += MERGED.format(pr["merged_by"], pr["merged_at"])
            # Otherwise
            else:
                embed.description += CLOSED.format(json["closed_by"], json["closed_at"])
        # If the Issue/PR is still open
        else:
            embed.description += OPEN

        # Finally, return the data
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(GitHub(bot))
