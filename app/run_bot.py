import sys
import os
import asyncio

sys.path.append(os.path.abspath(''))

from tg_bot.bot import main as run_bot

if __name__ == '__main__':
    asyncio.run(run_bot())