"""
Mukofotlar ro'yxati
"""

import logging
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.channel_check import require_membership

router = Router()
logger = logging.getLogger(__name__)

PRIZES_TEXT = """
🎁 <b>MUKOFOTLAR RO'YXATI</b>

🏆 <b>ASOSIY MUKOFOTLAR:</b>

🥇 <b>1-o'rin (100+ referral):</b>
• ✈️ Janubiy Koreyaga BEPUL sayohat (Seul + Jeju oroli, 10 kun)
• 🏛️ Degu universitetida 1 yil BEPUL koreys tili o'rganish
• 🏠 Degu universitetida BEPUL yotoqxona (1 yil)
• 📚 TOPIK 1-6 gacha professional tayyorgarlik kursi
• 🎓 Degu universiteti rasmiy sertifikati
• 📱 Samsung Galaxy telefon sovg'asi
• 🍜 Koreys taomlarini tayyorlash kursi (kimchi, bulgogi, bibimbap)

🥈 <b>2-o'rin (70+ referral):</b>
• 📖 6 oylik koreys tili kursi (TOPIK 1-4 gacha)
• 🎵 Online K-pop dance va qo'shiq darslari (BTS, BLACKPINK)
• 📚 Koreys tilini o'rganish uchun kitoblar to'plami
• 🎭 Hanbok (koreys milliy kiyimi) sovg'asi
• 🎬 K-drama serial tahlili master-klassi

🥉 <b>3-o'rin (50+ referral):</b>
• 📝 3 oylik koreys tili kursi (Hangeul + boshlang'ich grammatika)
• 🎪 Koreys madaniyati bo'yicha seminar (K-beauty, K-food)
• 🎁 K-pop aksessuarlar to'plami (BT21, TWICE sovg'alari)
• 📖 Koreys hikoyalari kitabi (ikki tilda)

🎯 <b>MAXSUS MUKOFOTLAR:</b>

🔥 <b>25+ referral:</b>
• 📝 1 oylik koreys tili kursi (Hangeul + oddiy gaplar)
• 📖 "안녕하세요 한국어" (Annyeonghaseyo Hangugeo) darsligi
• 🎵 K-pop qo'shiqlar orqali til o'rganish
• 🎮 Koreys tili o'yinlari to'plami

⭐ <b>10+ referral:</b>
• 📹 2 haftalik online video darslar
• 📜 Digital sertifikat (Hangeul alifbosini biluvchi)
• 🎪 "Koreys madaniyatiga sayohat" virtual tur
• 📱 Koreys tili o'rganish uchun mobil ilovalar

🎊 <b>5+ referral:</b>
• 📚 Haftalik koreys tili darsi (Hangeul alifbosi)
• 📖 E-book "Koreys tilining sirli dunyosi" (PDF)
• 🎭 Koreys an'analari haqida qisqa videolar
• 🍜 Oddiy koreys taomlarining retseptlari

📚 <b>BARCHA ISHTIROKCHILAR UCHUN:</b>
• 🔤 Bepul Hangeul alifbosi darslari (ㄱ, ㄴ, ㄷ...)
• 🎥 "Koreys tili nima?" online webinar
• 💬 Koreys tili o'rganuvchilar Telegram guruhi
• 🎼 K-pop qo'shiqlarning so'z ma'nolari

⏰ <b>KONKURS MUDDATI:</b>
31-yanvar 2025 gacha

📋 <b>SHARTLAR:</b>
• Telegram kanalimizga a'zo bo'lish majburiy
• Faqat haqiqiy foydalanuvchilar hisoblanadi
• G'oliblar 1-fevral kuni e'lon qilinadi
• Mukofotlar 7 kun ichida topshiriladi

🌟 <b>QO'SHIMCHA MA'LUMOT:</b>
• 👨‍🏫 Koreys tili darslari Janubiy Koreya universitetlari bitiruvchilari tomonidan o'tiladi
• 📜 Barcha kurslar xalqaro tan olingan sertifikat bilan yakunlanadi
• 📺 Online darslar jonli efir formatida (Zoom orqali)
• 🎯 TOPIK (Test of Proficiency in Korean) imtihoniga tayyorlash
• 🎵 K-pop qo'shiqlar va K-drama seriallar orqali til o'rganish metodikasi
• 🍜 Koreys taomlarini tayyorlash darslari praktik ko'rinishda
• 📱 Har bir o'quvchi uchun maxsus mobil ilova

🎭 <b>더 많은 친구를 초대하세요!</b> (Deo maneun chingureul chodaehaseyo!)
<i>Ko'proq do'st taklif qiling va koreys tilining ajoyib dunyosiga kirish imkoniyatini qo'lga kiriting!</i>
"""

@router.message(Command("prizes"))
@require_membership
async def prizes_command(message: types.Message):
    """Mukofotlar buyrug'i"""
    await show_prizes(message)

@router.callback_query(lambda c: c.data == "prizes")
@require_membership
async def prizes_callback(callback: types.CallbackQuery):
    """Mukofotlar callback"""
    await show_prizes(callback.message)
    await callback.answer()

async def show_prizes(message_obj):
    """Mukofotlar ro'yxatini ko'rsatish"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔗 Taklif havolam", callback_data="my_link")],
        [InlineKeyboardButton(text="📊 Statistikam", callback_data="my_stats")],
        [InlineKeyboardButton(text="🏆 Top reyting", callback_data="top_users")],
        [InlineKeyboardButton(text="🔙 Asosiy menyu", callback_data="main_menu")]
    ])
    
    if hasattr(message_obj, 'edit_text'):
        await message_obj.edit_text(PRIZES_TEXT, reply_markup=keyboard)
    else:
        await message_obj.answer(PRIZES_TEXT, reply_markup=keyboard)
      
