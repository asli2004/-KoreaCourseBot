"""
Referral havola bilan bog'liq funksiyalar
"""

import logging
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.channel_check import require_membership
from config import REFERRAL_URL_FORMAT

router = Router()
logger = logging.getLogger(__name__)

@router.message(Command("my_link"))
@require_membership
async def my_link_command(message: types.Message):
    """Foydalanuvchining shaxsiy taklif havolasini ko'rsatish"""
    await show_referral_link(message.from_user.id, message)

@router.callback_query(lambda c: c.data == "my_link")
@require_membership
async def my_link_callback(callback: types.CallbackQuery):
    """Taklif havolasi callback"""
    await show_referral_link(callback.from_user.id, callback.message)
    await callback.answer()

async def show_referral_link(user_id: int, message_obj):
    """Taklif havolasini ko'rsatish"""
    # Bot username'ini olish
    bot_info = await message_obj.bot.get_me()
    bot_username = bot_info.username
    
    # Referral havolasini yaratish
    referral_url = REFERRAL_URL_FORMAT.format(
        bot_username=bot_username,
        user_id=user_id
    )
    
    text = f"""
🔗 <b>Sizning shaxsiy taklif havolangiz:</b>

<code>{referral_url}</code>

  📋 <b>Qanday ishlatiladi:</b>
• Ushbu havolani do'stlaringiz bilan ulashing
• Har bir yangi a'zo sizning hisobingizga qo'shiladi
• Ko'proq do'st taklif qiling va mukofotlarga ega bo'ling!

💡 <b>Maslahat:</b> Havolani nusxa olish uchun ustiga bosing va "Copy" tugmasini bosing.
"""
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Statistikam", callback_data="my_stats")],
        [InlineKeyboardButton(text="🏆 Top reyting", callback_data="top_users")],
        [InlineKeyboardButton(text="🔙 Asosiy menyu", callback_data="main_menu")]
    ])
    
    if hasattr(message_obj, 'edit_text'):
        await message_obj.edit_text(text, reply_markup=keyboard)
    else:
        await message_obj.answer(text, reply_markup=keyboard)

@router.callback_query(lambda c: c.data == "main_menu")
async def main_menu_callback(callback: types.CallbackQuery):
    """Asosiy menyuga qaytish"""
    from utils.messages import START_MESSAGE
    from config import INSTAGRAM_URL
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔗 Mening taklif havolam", callback_data="my_link")],
        [InlineKeyboardButton(text="📊 Statistikam", callback_data="my_stats")],
        [InlineKeyboardButton(text="🏆 Top reyting", callback_data="top_users")],
        [InlineKeyboardButton(text="🎁 Mukofotlar", callback_data="prizes")],
        [InlineKeyboardButton(text="📱 Instagram sahifa", url=INSTAGRAM_URL)]
    ])
    
    await callback.message.edit_text(START_MESSAGE, reply_markup=keyboard)
    await callback.answer()
