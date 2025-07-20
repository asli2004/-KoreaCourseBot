"""
Top reyting bilan bog'liq funksiyalar
"""

import logging
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database import get_top_users
from utils.channel_check import require_membership

router = Router()
logger = logging.getLogger(__name__)

@router.message(Command("top"))
@require_membership
async def top_command(message: types.Message):
    """Top reyting buyrug'i"""
    await show_top_users(message, limit=10)

@router.callback_query(lambda c: c.data == "top_users")
@require_membership
async def top_callback(callback: types.CallbackQuery):
    """Top reyting callback"""
    await show_top_users(callback.message, limit=10)
    await callback.answer()

@router.callback_query(lambda c: c.data == "top_10")
@require_membership
async def top_10_callback(callback: types.CallbackQuery):
    """Top 10 callback"""
    await show_top_users(callback.message, limit=10)
    await callback.answer()

@router.callback_query(lambda c: c.data == "top_100")
@require_membership
async def top_100_callback(callback: types.CallbackQuery):
    """Top 100 callback"""
    await show_top_users(callback.message, limit=100)
    await callback.answer()

async def show_top_users(message_obj, limit: int = 10):
    """Top foydalanuvchilarni ko'rsatish"""
    top_users = await get_top_users(limit)
    
    if not top_users:
        text = """
🏆 <b>Top Reyting</b>

📝 <i>Hozircha hech kim referral qilmagan.</i>

Birinchi bo'ling va katta mukofotlarga ega bo'ling! 🎁
"""
    else:
        text = f"🏆 <b>Top {limit} Reyting</b>\n\n"
        
        medals = ["🥇", "🥈", "🥉"]
        
        for i, (user_id, first_name, username, referral_count) in enumerate(top_users, 1):
            if i <= 3:
                medal = medals[i-1]
            else:
                medal = f"{i}."
            
            name = first_name or "Anonim"
            username_text = f"@{username}" if username else ""
            
            text += f"{medal} {name} {username_text} - {referral_count} ta\n"
    
    # Keyboard yaratish
    keyboard_buttons = []
    
    if limit == 10:
        keyboard_buttons.append([InlineKeyboardButton(text="📈 Top 100", callback_data="top_100")])
    else:
        keyboard_buttons.append([InlineKeyboardButton(text="🔟 Top 10", callback_data="top_10")])
    
    keyboard_buttons.extend([
        [InlineKeyboardButton(text="📊 Mening statistikam", callback_data="my_stats")],
        [InlineKeyboardButton(text="🔗 Taklif havolam", callback_data="my_link")],
        [InlineKeyboardButton(text="🔙 Asosiy menyu", callback_data="main_menu")]
    ])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    
    if hasattr(message_obj, 'edit_text'):
        await message_obj.edit_text(text, reply_markup=keyboard)
    else:
        await message_obj.answer(text, reply_markup=keyboard)
