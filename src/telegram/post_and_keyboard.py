# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class PostAndKeyboard:
    @staticmethod
    async def keyb():
        _start_key = InlineKeyboardMarkup(row_width=1)

        _start_key.add(InlineKeyboardButton(text=f'Подписаться ❤️',
                                            url='https://vk.cc/crt0Q4'))

        _start_key.add(InlineKeyboardButton(text=f'Мировой рекорд и рекорд РФ ❤️',
                                            url='https://vk.cc/crt0HV'))

        _start_key.add(InlineKeyboardButton(text=f'Наш сайт 💚',
                                            url='https://vk.cc/crt0UG'))

        _start_key.add(InlineKeyboardButton(text=f'Проводник 🖤',
                                            url='https://vk.cc/4U3YyL'))

        return _start_key

    @staticmethod
    async def post_and_keyboard(call: types.CallbackQuery):
        _msg_temp = 'Мастер гвоздестояния 🕉 психолог 💟 проводник в мир честных ответов ❤️\n\n' \
                    '10 000 часов проведённых практик. Узнай подробнее по кнопке ниже👇'

        keb = await PostAndKeyboard.keyb()

        with open('src/telegram/1.jpg', 'rb') as file:
            await call.bot.send_photo('-1001864755804', file, caption=_msg_temp, reply_markup=keb)
