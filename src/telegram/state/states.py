from aiogram import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from pytube import YouTube

from settings import LOGO
from src.telegram.keyboard.keyboards import Admin_keyb
from src.telegram.sendler.sendler import Sendler_msg

from src.telegram.bot_core import BotDB


class States(StatesGroup):
    test = State()

    add_link = State()


async def test(message: Message, state: FSMContext):
    try:
        await message.bot.send_message(message.chat.id, 'Ответы приняты. Опрос окончен')
    except Exception as es:
        print(f'Ошибка {es}')

    await state.finish()


async def add_link(message: Message, state: FSMContext):
    link = message.text

    valid_video = True

    id_user = message.chat.id

    try:
        video = YouTube(link)
        preview = video.thumbnail_url
    except:
        valid_video = False

    if not valid_video:
        error = 'К сожалению, вы отправили ссылку не с YouTube, либо не подходящую ссылку.\nЧтобы ссылка заработала, ' \
                'зайдите на YouTube под видео, которое хотите скачать и скопируйте рабочую ссылку'

        keyb = Admin_keyb().start_keyb()

        await Sendler_msg().new_sendler_photo_message(message, LOGO, error, keyb)

        await state.finish()

        return False

    _msg = f'Выберите качество, в котором хотите скачать видео:'

    id_pk = BotDB.add_link(id_user, link)

    keyb = Admin_keyb().download_video(id_pk)

    await message.bot.send_photo(id_user, photo=preview, caption=_msg, reply_markup=keyb)

    await state.finish()


def register_state(dp: Dispatcher):
    dp.register_message_handler(test, state=States.test)

    dp.register_message_handler(add_link, state=States.add_link)
