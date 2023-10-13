import asyncio
import threading

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from pytube import YouTube

from settings import LOGO, VIDEO_TYPE, USER_BOT_NAME
from src.telegram.keyboard.keyboards import Admin_keyb
from src.telegram.logic.add_response_word import add_response_word
from src.telegram.logic.send_client_type_message import send_client_type_message
from src.telegram.sendler.sendler import Sendler_msg

from src.telegram.bot_core import BotDB
from src.youtube.download_mp3 import DownloadMp3


class States(StatesGroup):
    test = State()

    add_link = State()

    add_link_mp3 = State()

    mailing_set = State()


async def test(message: Message, state: FSMContext):
    try:
        await message.bot.send_message(message.chat.id, 'Ответы приняты. Опрос окончен')
    except Exception as es:
        print(f'Ошибка {es}')

    await state.finish()


async def search_type(video):
    good_type = []

    try:

        for _type in video.fmt_streams:

            type = str(_type.resolution)[:-1]

            if type in VIDEO_TYPE:
                good_type.append(int(type))

        if good_type != []:
            good_type = [x for x in set(good_type)]

            good_type = sorted(good_type)
    except:
        return VIDEO_TYPE

    return good_type


async def _send_audio(message: Message, text_user_name):
    try:
        await message.bot.send_audio(int(text_user_name), message.audio.file_id)
    except Exception as es:
        error = (f'Ошибка пр редиректе файла "{es}"')

        print(error)

        await Sendler_msg.sendler_to_admin(message, error, None)

        return False

    return True


async def _send_video(message: Message, text_user_name):
    try:
        await message.bot.send_video(int(text_user_name), message.video.file_id)
    except Exception as es:
        error = (f'Ошибка пр редиректе файла "{es}"')

        print(error)

        await Sendler_msg.sendler_to_admin(message, error, None)

        return False

    return True


async def check_user_bot(message: Message):
    text_user_name = message.text if message.text is not None else message.caption

    type_message = message.content_type

    if type_message == 'audio':
        res_ = await _send_audio(message, text_user_name)
    elif type_message == 'video':
        res_ = await _send_video(message, text_user_name)
    else:
        res_ = False

    if not res_:
        return False

    over_msg = f'Надеюсь, я смог вам помочь 🥺'

    keyb = Admin_keyb().start_keyb(text_user_name)

    await message.bot.send_message(int(text_user_name), over_msg, reply_markup=keyb)
    # await message.bot.send_photo(int(text_user_name), file, caption=over_msg, reply_markup=keyb)

    return True


async def add_link(message: Message, state: FSMContext):
    user_name = message.chat.username

    if user_name == USER_BOT_NAME[1:]:
        # Получение данных

        await check_user_bot(message)

        return True

    link = message.text

    valid_video = True

    id_user = message.chat.id

    one_msg = await message.bot.send_message(id_user, 'Определяю варианты качества видео...')

    try:
        video = YouTube(link)

        good_type = ['360', '480', '720', '1080']
        # good_type = await search_type(video)

        name_video = video.title

        name_channel = video.author

        preview = video.thumbnail_url
    except:
        valid_video = False

    if not valid_video:
        error = 'К сожалению, вы отправили ссылку не с YouTube, либо не подходящую ссылку.\nЧтобы ссылка заработала, ' \
                'зайдите на YouTube под видео, которое хотите скачать и скопируйте рабочую ссылку'

        keyb = Admin_keyb().start_keyb(id_user)

        try:
            await message.bot.delete_message(id_user, one_msg.message_id)
        except:
            pass

        await Sendler_msg().new_sendler_photo_message(message, LOGO, error, keyb)

        await state.finish()

        return False

    _msg = f'Выберите качество, в котором хотите скачать видео:\n\n' \
           f'🎥 {name_video}\n\n' \
           f'👨‍💻 {name_channel}'

    id_pk = BotDB.add_link(id_user, link)

    keyb = Admin_keyb().download_video(id_pk, good_type)

    try:
        await message.bot.delete_message(id_user, one_msg.message_id)
    except:
        pass

    await message.bot.send_photo(id_user, photo=preview, caption=_msg, reply_markup=keyb)

    await state.finish()


async def add_link_mp3(message: Message, state: FSMContext):
    link = message.text

    valid_video = True

    id_user = message.chat.id

    one_msg = await message.bot.send_message(id_user, 'Начинаю получать звуковой файл...')

    try:
        video = YouTube(link)
    except:
        valid_video = False

    if not valid_video:
        error = 'К сожалению, вы отправили ссылку не с YouTube, либо не подходящую ссылку.\nЧтобы ссылка заработала, ' \
                'зайдите на YouTube под видео, с которого хотите скачать звук и скопируйте рабочую ссылку'

        keyb = Admin_keyb().start_keyb(id_user)

        try:
            await message.bot.delete_message(id_user, one_msg.message_id)
        except:
            pass

        await Sendler_msg().new_sendler_photo_message(message, LOGO, error, keyb)

        await state.finish()

        return False

    name_file = video.title

    result_dict = {'result': False, 'filter': '360', 'link': link, 'one_msg_id': one_msg.message_id, 'id_user': id_user,
                   'name_file': name_file}

    trh = threading.Thread(target=DownloadMp3.start_down,
                           args=(result_dict, '', ''),
                           name=(f'thr-{id_user}'))

    trh.start()

    wait_download = asyncio.create_task(DownloadMp3.wait_download(result_dict, message))

    await state.finish()


async def mailing_set(message: Message, state: FSMContext):
    id_user = message.from_user.id

    id_pk_save_data = await add_response_word(message, 'False')

    row_sql_response = BotDB.get_response_word_from_id_pk(id_pk_save_data)

    id_pk = row_sql_response[0]

    keyb = Admin_keyb().approve_mailing_set(id_pk)

    await send_client_type_message(message, id_user, row_sql_response, keyb)

    await state.finish()


def register_state(dp: Dispatcher):
    dp.register_message_handler(test, state=States.test)

    dp.register_message_handler(add_link, state=States.add_link)

    dp.register_message_handler(add_link_mp3, state=States.add_link_mp3)

    dp.register_message_handler(mailing_set, state=States.mailing_set, content_types=[types.ContentType.ANY])
