import asyncio
import os

import re

import aiogram
import aiogram.utils
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API-KEY")

BOT = aiogram.Bot(token=API_TOKEN)

DISPATCHER = aiogram.Dispatcher()


def is_spammer_or_bot(message: aiogram.types.Message) -> bool:
    with open("spam_filter", "r") as filter:
        filter_words = filter.read().split(",")

        if any(keyword in message.text.lower() for keyword in filter_words):
            return True

        if re.search(r"http[s]?://", message.text.lower()):
            return True

        return False


@DISPATCHER.message_handler()
async def message_handle(message: aiogram.types.Message) -> None:
    if is_spammer_or_bot(message=message):

        await message.chat.ban(message.from_user.id)

        await message.delete()


@DISPATCHER.message_handler()
async def send_message() -> None:
    pass


if __name__ == "__main__":
    asyncio.run(DISPATCHER.start_polling(BOT))
