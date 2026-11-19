import asyncio
import logging
import sys

from meme_bot.bot import main

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
