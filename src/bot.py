import asyncio
import os
import httpx
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
XUI_BASE_URL = os.getenv("XUI_BASE_URL")
XUI_API_KEY = os.getenv("XUI_API_KEY")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("👋 Привет! Я бот для управления VPN через 3x-ui.\n"
                         "Отправь /users чтобы увидеть список пользователей.")

@dp.message(Command("users"))
async def get_users(message: types.Message):
    try:
        async with httpx.AsyncClient(verify=False) as client:
            headers = {"Authorization": XUI_API_KEY}
            response = await client.get(f"{XUI_BASE_URL}/panel/api/inbounds/list", headers=headers)
            data = response.json()
            users = [u["remark"] for inbound in data["obj"] for u in inbound.get("clientStats", [])]
            text = "👥 Пользователи:\n" + "\n".join(users) if users else "Пока нет активных пользователей."
            await message.answer(text)
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
