import aiogram
import asyncio

from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.state import State, StatesGroup
from app.handllers import router

API_TOKEN = '8178599573:AAEXyUs1WG3Hz56ZtF8t6cVKTu48o9XIiZA'







async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
