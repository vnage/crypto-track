import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo
from config import BOT_TOKEN, WEB_APP_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Open Portfolio", web_app=WebAppInfo(url=WEB_APP_URL))]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    
    await message.answer(
        " привет! это демо-трекер крипто-портфеля.\n\n"
        "нажми кнопку ниже, чтобы открыть приложение.\n"
        " все данные демонстрационные.",
        reply_markup=keyboard
    )

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "доступные команды:\n"
        "/start - главное меню\n"
        "/help - справка\n\n"
        "основной функционал доступен через mini app."
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("бот остановлен")
