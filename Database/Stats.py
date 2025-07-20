"""
Statistika bilan bog'liq funksiyalar
"""

import logging
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database import get_referral_stats, get_total_users_count
from utils.channel_check import require_membership

router = Router()
logger = logging.getLogger(__name__)

@router.message(Command("stats"))
@require_membership
async def stats_command(message: types.Message):
    """Statistika buyrug'i"""
    await show_user_stats(message.from_user.id, message)

@router.callback_query(lambda c: c.data == "my_stats")
@require_membership
async def stats_callback(callback: types.CallbackQuery):
    """Statistika callback"""
    await show_user_stats(callback.from_user.id, callback.message)
    await callback.answer()

async def show_user_stats(user_id: int, message_obj):
    """Foydalanuvchi statistikasini ko'rsatish"""
    stats = await get_referral_stats(user_id)
    total_users = await get_total_users_count()
    
    text = f"""
📊 <b>Sizning statistikangiz:</b>

👥 <b>Taklif qilgan odamlar soni:</b> {stats['total_count']}
🌍 <b>Jami bot foydalanuvchilari:</b> {total_users}

"""

if stats['recent_referrals']:
        text += "🆕 <b>So'nggi taklif qilganlar:</b>\n"
        for i, (name, username, created_at) in enumerate(stats['recent_referrals'][:5], 1):
            username_text = f"@{username}" if username else "Username yo'q"
            text += f"{i}. {name} ({username_text})\n"
    else:
        text += "📝 <i>Siz hali hech kimni taklif qilmagansiz.</i>\n"
    
    text += "\n💡 <b>Ko'proq do'st taklif qiling va mukofotlarga ega bo'ling!</b>"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔗 Taklif havolam", callback_data="my_link")],
        [InlineKeyboardButton(text="🏆 Top reyting", callback_data="top_users")],
        [InlineKeyboardButton(text="🔙 Asosiy menyu", callback_data="main_menu")]
    ])
    
    if hasattr(message_obj, 'edit_text'):
        await message_obj.edit_text(text, reply_markup=keyboard)
    else:
        await message_obj.answer(text, reply_markup=keyboard)
