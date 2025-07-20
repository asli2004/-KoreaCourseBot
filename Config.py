"""
Bot konfiguratsiyasi
"""

import os

# Bot Token (Telegram BotFather'dan olingan)
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# Majburiy kanal ID (masalan: @degu_university)
CHANNEL_ID = os.getenv("CHANNEL_ID", "@koreys_quiz")

# Instagram sahifa havolasi
INSTAGRAM_URL = os.getenv("INSTAGRAM_URL", "https://instagram.com/kores_tili_online")

# Ma'lumotlar bazasi fayl nomi
DATABASE_FILE = "bot_database.db"

# Bot admin ID'lari
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]

# Referral havola formati
REFERRAL_URL_FORMAT = "https://t.me/{bot_username}?start=ref_{user_id}"

# Top foydalanuvchilar soni
TOP_USERS_COUNT = 100
