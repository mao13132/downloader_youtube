from aiogram.types import Message

from aiogram import Dispatcher

from settings import LOGO
from src.telegram.keyboard.keyboards import Admin_keyb
from src.telegram.sendler.sendler import Sendler_msg

from src.telegram.bot_core import BotDB


async def start(message: Message):

    id_user = message.chat.id

    login = message.chat.username

    new_user = BotDB.check_or_add_user(id_user, login)

    user_name = message.chat.first_name if message.chat.first_name is not None else message.chat.username

    _msg = f'Здравствуйте {user_name}! Что вам от меня требуется?'

    keyb = Admin_keyb().start_keyb()

    await Sendler_msg().new_sendler_photo_message(message, LOGO, _msg, keyb)


def register_user(dp: Dispatcher):
    dp.register_message_handler(start, text_contains='/start')
