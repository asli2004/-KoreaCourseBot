#!/usr/bin/env python3
"""
Degu Universiteti Koreys Tili Konkursi Telegram Bot
Asosiy kirish nuqtasi
"""

import asyncio
import logging
import sys
from bot import main

# Logging konfiguratsiyasi
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('bot.log', encoding='utf-8')
    ]
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        logger.info("Bot ishga tushirilmoqda...")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot to'xtatildi")
    except Exception as e:
        logger.error(f"Botda xatolik yuz berdi: {e}")
        sys.exit(1) 
