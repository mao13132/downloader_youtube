from aiogram.types import Message

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram import types

from src.telegram.keyboard.keyboards import Admin_keyb
from src.telegram.logic._start import _start
from src.telegram.sendler.sendler import Sendler_msg
from settings import LOGO

from src.telegram.bot_core import BotDB


class UserKeyb:

    def subscriber(self, sub_link_channel):
        self._start_key = InlineKeyboardMarkup(row_width=1)

        self._start_key.add(InlineKeyboardButton(text='👉Подписаться', callback_data='link_sait',
                                                 url=sub_link_channel))
        self._start_key.add(InlineKeyboardButton(text=f'🌿 Я подписался', callback_data='check_group'))

        return self._start_key


async def check_group(call: types.CallbackQuery):
    await Sendler_msg.log_client_call(call)

    subs = await checking_for_a_subscription(call.message)

    if not subs:
        return False

    id_user = call.message.chat.id

    keyb = Admin_keyb().start_keyb(id_user)

    await call.bot.delete_message(call.message.chat.id, call.message.message_id)

    await _start(call.message)


async def checking_for_a_subscription(message: Message):
    type_chat = message.chat.type

    if type_chat != 'private':
        return True

    user_id = message.chat.id

    sub_status = BotDB.get_subs_status()

    if int(sub_status) == 0:
        return True

    user_data = BotDB.get_user_data_from_id(user_id)

    if not user_data:
        return False

    count_down_user = user_data[7]

    sub_id_channel = BotDB.get_id_subs_channel()

    sub_link_channel = BotDB.get_link_subs_channel()

    sub_count_down = BotDB.get_count_subs_file_down()

    sub_count_down = int(sub_count_down)

    if count_down_user < sub_count_down:
        return True

    try:
        response = await message.bot.get_chat_member(sub_id_channel, user_id)
    except Exception as es:
        if 'Chat not found' in str(es):
            name_bot = await message.bot.get_me()

            name_user = f'@{message.chat.username}' if message.chat.username is not None else message.chat.first_name

            error = (
                f'⚠️ Админка: Бот @{name_bot.username} не является админом канала "{sub_id_channel}"'
                f' на подписку которого идёт проверка. \n\n'
                f'Пропускаю {name_user} пользователя без подписки')

            print(error)

            await Sendler_msg.sendler_to_admin(message, error, None)

            return True

        print(f'Ошибка получения статуса подписчика "{es}"')
        return False

    if response['status'] == 'left':
        print(f'User: {user_id} не подписан на группу')

        text_admin = f'🙂 {message.chat.full_name}, что бы воспользоваться мной, ' \
                     f'Вы должны быть подписаны на наш канал\n\n' \
                     f'Жми что бы подписаться👇'

        keyb = UserKeyb().subscriber(sub_link_channel)

        await Sendler_msg.send_msg_message(message, text_admin, keyb)

        return False

    return True  # Подписан
