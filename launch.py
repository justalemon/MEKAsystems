import argparse
import logging
import os

from bot import MEKAsystems

logger = logging.getLogger("MEKAsystems")
logger.setLevel(logging.INFO)


def run_bot(token, mongourl, prefix):
    # Create an instance of the bot with the prefix and mongo url
    bot = MEKAsystems(prefix, mongourl=mongourl)

    # Start loading the extensions
    logger.info("Loading extensions form 'ext'")
    # For each file in the ext folder
    for file in os.listdir("ext"):
        # If is a Python file
        if file.endswith(".py"):
            # Notify the user that we are loading the extension
            logger.info("Loading cogs from {0}".format(file))
            # And then load the Python file without the extension
            bot.load_extension("ext." + os.path.splitext(file)[0])

    # Finally, run the bot with the specified token
    bot.run(token)


def main():
    # Create an argument parser with the required arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", dest="env", action="store_true",
                        help="if the Bot should be configured with the environment variables")
    # And parse those arguments
    args = parser.parse_args()

    # Add a stream handler for the bot logger
    logger.addHandler(logging.StreamHandler())

    # If the user wants to use the the environment variables
    if args.env:
        # Notify it
        logger.info("Starting the Bot on environment variables mode")
        # Get the values from the environment variables
        token = os.environ.get("DISCORD_TOKEN")
        prefix = os.environ.get("DISCORD_PREFIX", "&")
        mongourl = os.environ.get("MONGODB_URL")
        # And start the Bot with those variables
        run_bot(token, mongourl, prefix)


if __name__ == "__main__":
    main()
