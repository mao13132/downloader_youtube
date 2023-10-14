from aiogram.types import Message

from aiogram import Dispatcher, types

from settings import LOGO, USER_BOT_NAME, ADMIN
from src.telegram.keyboard.keyboards import Admin_keyb
from src.telegram.logic.checking_for_a_subscription import checking_for_a_subscription
from src.telegram.sendler.sendler import Sendler_msg

from src.telegram.bot_core import BotDB
from src.telegram.state.states import add_link


async def start(message: Message):
    id_user = message.chat.id

    login = message.chat.username

    new_user = BotDB.check_or_add_user(id_user, login)

    subs = await checking_for_a_subscription(message)

    if not subs:
        return False

    user_name = message.chat.first_name if message.chat.first_name is not None else message.chat.username

    _msg = f'Здравствуйте {user_name}! Что вам от меня требуется?'

    keyb = Admin_keyb().start_keyb(id_user)

    await Sendler_msg().new_sendler_photo_message(message, LOGO, _msg, keyb)


async def test(message: Message):
    login_user = f"@{message.from_user.username}" if message.from_user.username is not None else message.from_user.id


async def _new_chat_members(message: Message):
    login_user = f"@{message.from_user.username}" if message.from_user.username is not None else message.from_user.id

    chat_name = message.chat.full_name if message.chat.full_name is not None else message.chat.id

    _msg = f'Пользователь: {login_user} подписался на канал {chat_name}'

    print(f'Поступило служебное сообщение "{_msg}"')

    await Sendler_msg.sendler_to_admin_mute(message, _msg, None)


def register_user(dp: Dispatcher):
    dp.register_message_handler(start, text_contains='/start')

    dp.register_message_handler(_new_chat_members, content_types=['new_chat_members'])

    dp.register_message_handler(add_link, text_contains='', content_types=[types.ContentType.ANY])


    dp.register_message_handler(test, text_contains='')
