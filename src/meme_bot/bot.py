import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from meme_bot.config import settings
from meme_bot.handlers import common_router, meme_router

logger = logging.getLogger(__name__)


async def main() -> None:
    bot = Bot(token=settings.token)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(common_router)
    dp.include_router(meme_router)
    logger.info("Starting meme-bot polling")
    await dp.start_polling(bot)
