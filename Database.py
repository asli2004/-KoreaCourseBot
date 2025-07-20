"""
Ma'lumotlar bazasi bilan ishlash
"""

import aiosqlite
import logging
from typing import List, Tuple, Optional
from config import DATABASE_FILE

logger = logging.getLogger(__name__)

async def init_database():
    """Ma'lumotlar bazasini yaratish va jadvallarni sozlash"""
    async with aiosqlite.connect(DATABASE_FILE) as db:
        # Foydalanuvchilar jadvali
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                referred_by INTEGER,
                referral_count INTEGER DEFAULT 0,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_member BOOLEAN DEFAULT FALSE,
                instagram_confirmed BOOLEAN DEFAULT FALSE
            )
        """)
        
        # Referrallar jadvali
        await db.execute("""
            CREATE TABLE IF NOT EXISTS referrals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                referrer_id INTEGER,
                referred_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (referrer_id) REFERENCES users (user_id),
                FOREIGN KEY (referred_id) REFERENCES users (user_id)
            )
        """)

        await db.commit()
        logger.info("Ma'lumotlar bazasi muvaffaqiyatli yaratildi")

async def add_user(user_id: int, username: str = None, first_name: str = None, 
                   last_name: str = None, referred_by: int = None) -> bool:
    """Yangi foydalanuvchi qo'shish"""
    try:
        async with aiosqlite.connect(DATABASE_FILE) as db:
            # Foydalanuvchi mavjudligini tekshirish
            cursor = await db.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
            if await cursor.fetchone():
                return False  # Foydalanuvchi allaqachon mavjud
            
            # Yangi foydalanuvchi qo'shish
            await db.execute("""
                INSERT INTO users (user_id, username, first_name, last_name, referred_by)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, username, first_name, last_name, referred_by))
            
            # Agar referral orqali kelgan bo'lsa, referrerning statistikasini yangilash
            if referred_by:
                await db.execute("""
                    INSERT INTO referrals (referrer_id, referred_id) VALUES (?, ?)
                """, (referred_by, user_id))
                
                await db.execute("""
                    UPDATE users SET referral_count = referral_count + 1 
                    WHERE user_id = ?
                """, (referred_by,))

await db.commit()
            logger.info(f"Yangi foydalanuvchi qo'shildi: {user_id}")
            return True
    except Exception as e:
        logger.error(f"Foydalanuvchi qo'shishda xatolik: {e}")
        return False

async def get_user(user_id: int) -> Optional[dict]:
    """Foydalanuvchi ma'lumotlarini olish"""
    try:
        async with aiosqlite.connect(DATABASE_FILE) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("""
                SELECT * FROM users WHERE user_id = ?
            """, (user_id,))
            row = await cursor.fetchone()
            return dict(row) if row else None
    except Exception as e:
        logger.error(f"Foydalanuvchi ma'lumotlarini olishda xatolik: {e}")
        return None

async def update_member_status(user_id: int, is_member: bool):
    """Foydalanuvchining kanal a'zoligi holatini yangilash"""
    try:
        async with aiosqlite.connect(DATABASE_FILE) as db:
            await db.execute("""
                UPDATE users SET is_member = ? WHERE user_id = ?
            """, (is_member, user_id))
            await db.commit()
    except Exception as e:
        logger.error(f"A'zolik holatini yangilashda xatolik: {e}")

async def update_instagram_status(user_id: int, instagram_confirmed: bool):
    """Foydalanuvchining Instagram obunasi holatini yangilash"""
    try:
        async with aiosqlite.connect(DATABASE_FILE) as db:
            await db.execute("""
                UPDATE users SET instagram_confirmed = ? WHERE user_id = ?
            """, (instagram_confirmed, user_id))
            await db.commit()
    except Exception as e:
        logger.error(f"Instagram holati yangilashda xatolik: {e}")

async def check_full_membership(user_id: int) -> bool:
    """Foydalanuvchining to'liq a'zoligi (Telegram + Instagram) ni tekshirish"""
    try:
        async with aiosqlite.connect(DATABASE_FILE) as db:
            cursor = await db.execute("""
                SELECT is_member, instagram_confirmed FROM users WHERE user_id = ?
            """, (user_id,))
            row = await cursor.fetchone()
            if row:
                is_member, instagram_confirmed = row
                return is_member and instagram_confirmed
            return False
    except Exception as e:
        logger.error(f"To'liq a'zolik tekshirishda xatolik: {e}")
        return False

async def get_referral_stats(user_id: int) -> dict:
    """Foydalanuvchining referral statistikasini olish"""
    try:
        async with aiosqlite.connect(DATABASE_FILE) as db:
            cursor = await db.execute("""
                SELECT referral_count FROM users WHERE user_id = ?
            """, (user_id,))
            row = await cursor.fetchone()
            count = row[0] if row else 0
            
            cursor = await db.execute("""
                SELECT u.first_name, u.username, r.created_at 
                FROM referrals r
                JOIN users u ON r.referred_id = u.user_id
                WHERE r.referrer_id = ?
                ORDER BY r.created_at DESC
                LIMIT 10
            """, (user_id,))
            recent_referrals = await cursor.fetchall()
            
            return {
                "total_count": count,
                "recent_referrals": recent_referrals
            }
    except Exception as e:
        logger.error(f"Referral statistikasini olishda xatolik: {e}")
        return {"total_count": 0, "recent_referrals": []}

async def get_top_users(limit: int = 10) -> List[Tuple]:
    """Eng ko'p referral qilgan foydalanuvchilar ro'yxati"""
    try:
        async with aiosqlite.connect(DATABASE_FILE) as db:
            cursor = await db.execute("""
                SELECT user_id, first_name, username, referral_count
                FROM users 
                WHERE referral_count > 0
                ORDER BY referral_count DESC, joined_at ASC
                LIMIT ?
            """, (limit,))
            return await cursor.fetchall()
    except Exception as e:
        logger.error(f"Top foydalanuvchilarni olishda xatolik: {e}")
        return []

async def get_total_users_count() -> int:
    """Jami foydalanuvchilar sonini olish"""
  try:
        async with aiosqlite.connect(DATABASE_FILE) as db:
            cursor = await db.execute("SELECT COUNT(*) FROM users")
            row = await cursor.fetchone()
            return row[0] if row else 0
    except Exception as e:
        logger.error(f"Foydalanuvchilar sonini olishda xatolik: {e}")
        return 0
