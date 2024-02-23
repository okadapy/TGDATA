from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters.command import CommandStart
from aiogram.types import Message, ContentType
from app.database.requests import get_channel_data
from app.data_collector import collect_from_link
from config import BOT_TOKEN
import re

tg_link_re = re.compile(r"t\.me\/\+[a-zA-Z0-9]*")
bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()


async def start():
    await dp.start_polling(bot)


@dp.message(CommandStart())
async def handle_command_start(message: Message):
    await message.answer(
        text="Добрый день! Данный бот предоставляет возможность собрать публичную статитику о ТГ канале.\n\n\
            Для того, что бы воспользоваться функционалом, отправьте сообщение в чат."
    )


@dp.message(F.content_type == ContentType.TEXT)
async def handle_existing_entry(message: Message):
    link = tg_link_re.findall(message.text)
    if not any(link) or link is None:
        await message.answer("Проверьте правильность ввода ссылки.")
        return
    
    link = link[0]

    data = await get_channel_data(link)
    if data is None:
        try: 
            await collect_from_link(link)
        except Exception:
            await message.answer("Проверьте правильность ввода ссылки.")
            return
        
        data = await get_channel_data(link)
    await message.answer(data)
