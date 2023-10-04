from aiogram import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from pytube import YouTube

from settings import LOGO, VIDEO_TYPE
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


async def search_type(video):
    good_type = []

    for _type in video.fmt_streams:

        type = str(_type.resolution)[:-1]

        if type in VIDEO_TYPE:
            good_type.append(int(type))

    if good_type != []:
        good_type = sorted(good_type)
        good_type = set(good_type)

    return good_type


async def add_link(message: Message, state: FSMContext):
    link = message.text

    valid_video = True

    id_user = message.chat.id

    one_msg = await message.bot.send_message(id_user, 'Определяю варианты качества видео...')

    try:
        video = YouTube(link)

        good_type = await search_type(video)

        preview = video.thumbnail_url
    except:
        valid_video = False

    if not valid_video:
        error = 'К сожалению, вы отправили ссылку не с YouTube, либо не подходящую ссылку.\nЧтобы ссылка заработала, ' \
                'зайдите на YouTube под видео, которое хотите скачать и скопируйте рабочую ссылку'

        keyb = Admin_keyb().start_keyb()

        # await Sendler_msg().new_sendler_photo_message(message, LOGO, error, keyb)

        await message.bot.edit_message_text(error, id_user, one_msg.message_id)

        await state.finish()

        return False

    _msg = f'Выберите качество, в котором хотите скачать видео:'

    id_pk = BotDB.add_link(id_user, link)

    keyb = Admin_keyb().download_video(id_pk, good_type)

    try:
        await message.bot.delete_message(id_user, one_msg.message_id)
    except:
        pass

    await message.bot.send_photo(id_user, photo=preview, caption=_msg, reply_markup=keyb)

    await state.finish()


def register_state(dp: Dispatcher):
    dp.register_message_handler(test, state=States.test)

    dp.register_message_handler(add_link, state=States.add_link)
