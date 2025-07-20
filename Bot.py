"""
Asosiy bot konfiguratsiyasi va ishga tushirish
"""

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from database import init_database
from handlers import start, referral, stats, top, prizes

logger = logging.getLogger(__name__)

async def main():
    """Bot ishga tushirish funksiyasi"""

# Ma'lumotlar bazasini yaratish
    await init_database()
    
    # Bot va Dispatcher yaratish
    bot = Bot(
        token=BOT_TOKEN,
default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    dp = Dispatcher(storage=MemoryStorage())
    
    # Handlerlarni ro'yxatdan o'tkazish
    dp.include_router(start.router)
    dp.include_router(referral.router)
    dp.include_router(stats.router)
    dp.include_router(top.router)
    dp.include_router(prizes.router)
    
    try:
        logger.info("Bot polling boshlandi...")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
  asyncio.run(main())
