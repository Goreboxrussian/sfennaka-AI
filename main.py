import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.utils.markdown import hcode
from aiogram.filters import Command
import asyncio
import requests
import json
from config import BOT_TOKEN, OPENROUTER_API_KEY

bot = Bot(token=BOT_TOKEN, default=types.DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("👋 Привет! Напиши мне любой вопрос, и я передам его нейросети Qwen.")

@dp.message(Command("reset"))
async def reset_handler(message: Message):
    await message.answer("🔁 Контекст сброшен (но в этой версии контекста нет).")

@dp.message()
async def handle_message(message: Message):
    user_input = message.text
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            data=json.dumps({
                "model": "qwen/qwen3-32b:free",
                "messages": [
                    {
                        "role": "user",
                        "content": user_input
                    }
                ]
            })
        )

        result = response.json()
        reply = result["choices"][0]["message"]["content"]
        await message.answer(reply)
    except Exception as e:
        logging.exception("Ошибка при обращении к API:")
        await message.answer("Произошла ошибка при обработке запроса. Попробуйте позже.")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
