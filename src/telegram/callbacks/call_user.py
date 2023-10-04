import asyncio
import threading

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext

from src.telegram.logic.devision_msg import division_message
from src.telegram.handlers.users import start
from src.telegram.logic.good_mal import good_mal
from src.telegram.sendler.sendler import *

from src.telegram.keyboard.keyboards import *
from src.telegram.state.states import States

from src.telegram.bot_core import BotDB

from src.youtube.download_video import DownloadVideo


async def over_state(call: types.CallbackQuery, state: FSMContext):
    await state.finish()

    id_user = call.message.chat.id

    user_name = call.message.chat.first_name if call.message.chat.first_name is not None else call.message.chat.username

    _msg = f'Здравствуйте {user_name}! Что вам требуется от бота?'

    keyb = Admin_keyb().start_keyb(id_user)

    await Sendler_msg().sendler_photo_call(call, LOGO, _msg, keyb)


async def youtube(call: types.CallbackQuery, state: FSMContext):
    _msg = f'Вставьте ссылку на видео с YouTube что бы получить видеофайл'

    keyb = Admin_keyb().youtube()

    await Sendler_msg().sendler_photo_call(call, LOGO, _msg, keyb)

    await States.add_link.set()


async def mp3(call: types.CallbackQuery, state: FSMContext):
    _msg = f'Вставьте ссылку на видео с YouTube для получения звука с видео'

    keyb = Admin_keyb().youtube()

    await Sendler_msg().sendler_photo_call(call, LOGO, _msg, keyb)

    await States.add_link_mp3.set()


async def download(call: types.CallbackQuery, state: FSMContext):
    await state.finish()

    try:

        _, _filter, id_pk = str(call.data).split('-')

    except Exception as es:

        print(f'Ошибка при разборе для download call{es}')

        return False

    id_user = call.message.chat.id

    link = BotDB.get_link(id_pk)

    _msg = f'Скачивание началось...'

    await Sendler_msg().sendler_photo_call(call, LOGO, _msg, None)

    result_dict = {'result': False, 'filter': _filter, 'link': link}

    trh = threading.Thread(target=DownloadVideo.start_down,
                           args=(call, _filter, link, result_dict),
                           name=(f'thr-{id_user}'))

    trh.start()

    wait_download = asyncio.create_task(DownloadVideo.wait_download(result_dict, call))


async def admin_panel(call: types.CallbackQuery, state: FSMContext):
    id_user = call.message.chat.id

    await state.finish()

    await Sendler_msg.log_client_call(call)

    keyb = Admin_keyb().admin_panel()

    text_admin = 'Админ панель:'

    await Sendler_msg().sendler_photo_call(call, LOGO, text_admin, keyb)


async def over_state(call: types.CallbackQuery, state: FSMContext):
    await state.finish()

    await Sendler_msg.log_client_call(call)

    await call.message.bot.delete_message(call.message.chat.id, call.message.message_id)

    await start(call.message)


async def users(call: types.CallbackQuery):
    await Sendler_msg.log_client_call(call)

    list_all_users = BotDB.get_all_users()

    keyb = Admin_keyb().admin_back()

    _msg = 'Список пользователей\n\n'

    if list_all_users == []:
        _msg = '⛔️ Список пользователей пуст'

        await Sendler_msg().sendler_photo_call(call, LOGO, _msg, keyb)

        return False

    _msg += '\n\n'.join(f"Логин: @{x[2]} ID: {x[1]}" for x in list_all_users)

    if len(_msg) < 4096:
        await Sendler_msg().sendler_photo_call(call, LOGO, _msg, keyb)
    else:
        await division_message(call.message, _msg, keyb)


async def mailing_set(call: types.CallbackQuery):
    await Sendler_msg.log_client_call(call)

    _msg = f'🙇‍♀️Пришлите мне сообщение которое необходимо разослать всем пользователям'

    keyb = Admin_keyb().send_client()

    await Sendler_msg().sendler_photo_call(call, LOGO, _msg, keyb)

    await States.mailing_set.set()


def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(youtube, text='youtube')

    dp.register_callback_query_handler(mp3, text='mp3')

    dp.register_callback_query_handler(over_state, text='over_state', state='*')

    dp.register_callback_query_handler(download, text_contains='download', state='*')

    dp.register_callback_query_handler(admin_panel, text_contains='admin_panel', state='*')

    dp.register_callback_query_handler(over_state, text_contains='over_state', state='*')

    dp.register_callback_query_handler(users, text_contains='users')

    dp.register_callback_query_handler(mailing_set, text='mailing_set')

    dp.register_callback_query_handler(good_mal, text_contains='good_mal-')
