"""
/start buyrug'ini boshqarish
"""

import logging
from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database import add_user, get_user, update_instagram_status, check_full_membership
from utils.channel_check import check_channel_membership
from utils.messages import START_MESSAGE, CHANNEL_JOIN_MESSAGE
from config import CHANNEL_ID, INSTAGRAM_URL

router = Router()
logger = logging.getLogger(__name__)

@router.message(CommandStart())
async def start_handler(message: types.Message):
    """Start buyrug'ini qayta ishlash"""
    user = message.from_user
    user_id = user.id
    
    # Referral parametrini tekshirish
    args = message.text.split()[1:] if len(message.text.split()) > 1 else []
    referred_by = None
    
    if args and args[0].startswith("ref_"):
        try:
            referred_by = int(args[0][4:])  # "ref_" qismini olib tashlash
        except ValueError:
            pass
    
    # Foydalanuvchini ma'lumotlar bazasiga qo'shish
    user_data = await get_user(user_id)
    if not user_data:
        await add_user(
            user_id=user_id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            referred_by=referred_by
        )
        logger.info(f"Yangi foydalanuvchi: {user_id}, referrer: {referred_by}")

    # Kanal a'zoligini tekshirish
    is_member = await check_channel_membership(message.bot, user_id, CHANNEL_ID)
    
    # Agar a'zolik holati tekshirib bo'lmasa yoki a'zo bo'lmasa
    if is_member is False or is_member is None:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📢 Telegram kanalga a'zo bo'lish", url=f"https://t.me/{CHANNEL_ID[1:]}")],
            [InlineKeyboardButton(text="📱 Instagram sahifaga obuna bo'lish", url=INSTAGRAM_URL)],
            [InlineKeyboardButton(text="✅ A'zolikni tekshirish", callback_data="check_membership")]
        ])
        await message.answer(CHANNEL_JOIN_MESSAGE, reply_markup=keyboard)
        return
    
    # Asosiy menyu
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔗 Mening taklif havolam", callback_data="my_link")],
        [InlineKeyboardButton(text="📊 Statistikam", callback_data="my_stats")],
        [InlineKeyboardButton(text="🏆 Top reyting", callback_data="top_users")],
        [InlineKeyboardButton(text="🎁 Mukofotlar", callback_data="prizes")],
        [InlineKeyboardButton(text="📱 Instagram sahifa", url=INSTAGRAM_URL)]
    ])
    
    await message.answer(START_MESSAGE, reply_markup=keyboard)

@router.callback_query(lambda c: c.data == "check_membership")
async def check_membership_callback(callback: types.CallbackQuery):
    """A'zolikni tekshirish callback"""
    user_id = callback.from_user.id
    
    # Telegram kanal a'zoligini tekshirish
    is_member = await check_channel_membership(callback.bot, user_id, CHANNEL_ID)
    
    if is_member is None:
        # Bot a'zolikni tekshira olmaydi, foydalanuvchiga o'zi tasdiqlashni so'raymiz
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Ha, Telegram kanalga a'zo bo'ldim", callback_data="confirm_telegram")],
            [InlineKeyboardButton(text="📢 Kanalga a'zo bo'lish", url=f"https://t.me/{CHANNEL_ID[1:]}")],
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_start")]
        ])
        
        message_text = """
🔍 <b>Telegram kanal a'zoligini tekshirish:</b>

Agar siz bizning Telegram kanalimizga a'zo bo'lgan bo'lsangiz, "Ha, Telegram kanalga a'zo bo'ldim" tugmasini bosing.

Agar a'zo bo'lmagan bo'lsangiz, avval "Kanalga a'zo bo'lish" tugmasini bosib a'zo bo'ling, keyin qaytib keling.

<i>Eslatma: Botni to'liq ishlatish uchun Telegram kanal va Instagram sahifaga a'zo bo'lish majburiy!</i>
"""
        
        await callback.message.edit_text(message_text, reply_markup=keyboard)
        await callback.answer("📋 Iltimos, a'zolikni o'zingiz tasdiqlang")
        return
    
    elif not is_member:
        await callback.answer("❌ Siz hali Telegram kanalimizga a'zo bo'lmagansiz!", show_alert=True)
        return
    
    # Instagram obunasi haqida so'rash
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Ha, Instagram'ga obuna bo'ldim", callback_data="confirm_instagram")],
        [InlineKeyboardButton(text="📱 Instagram sahifaga o'tish", url=INSTAGRAM_URL)],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_start")]
    ])

message_text = """
✅ <b>Telegram kanal a'zoligi tasdiqlandi!</b>

📱 <b>Instagram obunasini tekshiring:</b>

Agar siz Instagram sahifamizga obuna bo'lgan bo'lsangiz, "Ha, Instagram'ga obuna bo'ldim" tugmasini bosing.

Agar obuna bo'lmagan bo'lsangiz, avval Instagram sahifaga o'ting va obuna bo'ling, keyin qaytib keling.
"""
    
    await callback.message.edit_text(message_text, reply_markup=keyboard)
    await callback.answer("✅ Telegram a'zolik tasdiqlandi!")

@router.callback_query(lambda c: c.data == "confirm_telegram")
async def confirm_telegram_callback(callback: types.CallbackQuery):
    """Telegram a'zoligini tasdiqlash (bot tekshira olmasa)"""
    user_id = callback.from_user.id
    
    # Foydalanuvchi o'zi tasdiqlayotgani uchun ma'lumotlar bazasini yangilaymiz
    from database import update_member_status
    await update_member_status(user_id, True)
    
    # Instagram obunasi haqida so'rash
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Ha, Instagram'ga obuna bo'ldim", callback_data="confirm_instagram")],
        [InlineKeyboardButton(text="📱 Instagram sahifaga o'tish", url=INSTAGRAM_URL)],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_start")]
    ])
    
    message_text = """
✅ <b>Telegram kanal a'zoligi tasdiqlandi!</b>

📱 <b>Instagram obunasini tekshiring:</b>

Agar siz Instagram sahifamizga obuna bo'lgan bo'lsangiz, "Ha, Instagram'ga obuna bo'ldim" tugmasini bosing.

Agar obuna bo'lmagan bo'lsangiz, avval Instagram sahifaga o'ting va obuna bo'ling, keyin qaytib keling.
"""
    
    await callback.message.edit_text(message_text, reply_markup=keyboard)
    await callback.answer("✅ Telegram a'zolik tasdiqlandi!")

@router.callback_query(lambda c: c.data == "confirm_instagram")
async def confirm_instagram_callback(callback: types.CallbackQuery):
    """Instagram obunasini tasdiqlash"""
    user_id = callback.from_user.id
    
    # Instagram obunasini ma'lumotlar bazasida saqlash
    await update_instagram_status(user_id, True)
    
    # Asosiy menyu ko'rsatish
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔗 Mening taklif havolam", callback_data="my_link")],
        [InlineKeyboardButton(text="📊 Statistikam", callback_data="my_stats")],
        [InlineKeyboardButton(text="🏆 Top reyting", callback_data="top_users")],
        [InlineKeyboardButton(text="🎁 Mukofotlar", callback_data="prizes")],
        [InlineKeyboardButton(text="📱 Instagram sahifa", url=INSTAGRAM_URL)]
    ])
    
    await callback.message.edit_text(START_MESSAGE, reply_markup=keyboard)
    await callback.answer("🎉 Barcha shartlar bajarildi! Konkursda ishtirok etishingiz mumkin!")

@router.callback_query(lambda c: c.data == "back_to_start")
async def back_to_start_callback(callback: types.CallbackQuery):
    """Boshiga qaytish"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Telegram kanalga a'zo bo'lish", url=f"https://t.me/{CHANNEL_ID[1:]}")],
        [InlineKeyboardButton(text="📱 Instagram sahifaga obuna bo'lish", url=INSTAGRAM_URL)],
        [InlineKeyboardButton(text="✅ A'zolikni tekshirish", callback_data="check_membership")]
    ])
    
    from utils.messages import CHANNEL_JOIN_MESSAGE
    await callback.message.edit_text(CHANNEL_JOIN_MESSAGE, reply_markup=keyboard)
    await callback.answer()
