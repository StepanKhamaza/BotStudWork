from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import asyncio
from get_data import get_messages

from config import bot_token
from config import channel_id

bot = Bot(bot_token)
dp = Dispatcher(bot)

@dp.message_handler()
async def send_message():
    while True:
        messages = get_messages();
        for i in range(len(messages)):
            await bot.send_message(channel_id, messages[i])
            await asyncio.sleep(3)

async def main():
    await send_message()

if __name__ == '__main__':
    executor.start(dp, main())