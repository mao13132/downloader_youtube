import asyncio
import threading

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ChatActions

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
    _msg = f'Вставьте ссылку на видео с YouTube, чтобы получить видеофайл 🎥'

    keyb = Admin_keyb().youtube()

    await Sendler_msg().sendler_photo_call(call, LOGO, _msg, keyb)

    await States.add_link.set()


async def support(call: types.CallbackQuery, state: FSMContext):
    await call.bot.answer_callback_query(call.id)

    _msg = f'Какой телефон вы используете?'

    keyb = Admin_keyb().system()

    await Sendler_msg().sendler_photo_call(call, LOGO, _msg, keyb)


async def mp3(call: types.CallbackQuery, state: FSMContext):
    await call.bot.answer_callback_query(call.id)

    _msg = f'Вставьте ссылку на видео с YouTube для получения звука с видео'

    keyb = Admin_keyb().youtube()

    await Sendler_msg().sendler_photo_call(call, LOGO, _msg, keyb)

    await States.add_link_mp3.set()


async def download(call: types.CallbackQuery, state: FSMContext):
    await state.finish()

    await call.bot.answer_callback_query(call.id)

    try:

        _, _filter, id_pk = str(call.data).split('-')

    except Exception as es:

        print(f'Ошибка при разборе для download call{es}')

        return False

    id_user = call.message.chat.id

    link = BotDB.get_link(id_pk)

    _msg = f'<b>Lizard качает ваше видео 🎬</b>\nЭто может занять от 10 секунд до 5 минут 🛜'

    await Sendler_msg().sendler_photo_call(call, LOGO, _msg, None)

    result_dict = {'result': False, 'filter': _filter, 'link': link, 'id_user': id_user}

    trh = threading.Thread(target=DownloadVideo.start_down,
                           args=(call, _filter, link, result_dict),
                           name=(f'thr-{id_user}'))

    trh.start()

    wait_download = asyncio.create_task(DownloadVideo.wait_download(result_dict, call))


async def admin_panel(call: types.CallbackQuery, state: FSMContext):
    await call.bot.answer_callback_query(call.id)

    id_user = call.message.chat.id

    await state.finish()

    await Sendler_msg.log_client_call(call)

    keyb = Admin_keyb().admin_panel()

    text_admin = 'Админ панель:'

    await Sendler_msg().sendler_photo_call(call, LOGO, text_admin, keyb)


async def over_state(call: types.CallbackQuery, state: FSMContext):
    await call.bot.answer_callback_query(call.id)

    await state.finish()

    await Sendler_msg.log_client_call(call)

    await call.message.bot.delete_message(call.message.chat.id, call.message.message_id)

    await start(call.message)


async def users(call: types.CallbackQuery):
    await call.bot.answer_callback_query(call.id)

    await Sendler_msg.log_client_call(call)

    list_all_users = BotDB.get_all_users()

    keyb = Admin_keyb().admin_back()

    _msg = 'Список пользователей\n\n'

    if list_all_users == []:
        _msg = '⛔️ Список пользователей пуст'

        await Sendler_msg().sendler_photo_call(call, LOGO, _msg, keyb)

        return False

    _msg += '\n\n'.join(f"{count + 1}. Логин: {f'@{x[2]}' if x[2] is not None else 'Не указан'} ID: {x[1]}"
                        for count, x in enumerate(list_all_users))

    msg_ = _msg.replace('\n', '')

    if len(msg_) < 1024:
        await Sendler_msg().sendler_photo_call(call, LOGO, _msg, keyb)
    else:
        await division_message(call.message, _msg, keyb)


async def mailing_set(call: types.CallbackQuery):
    await Sendler_msg.log_client_call(call)

    _msg = f'🙇‍♀️Пришлите мне сообщение которое необходимо разослать всем пользователям'

    keyb = Admin_keyb().send_client()

    await Sendler_msg().sendler_photo_call(call, LOGO, _msg, keyb)

    await States.mailing_set.set()


async def instruction(call: types.CallbackQuery, state: FSMContext):
    await call.bot.answer_callback_query(call.id)

    await state.finish()

    try:

        _, user_system = str(call.data).split('-')

    except Exception as es:

        print(f'Ошибка при разборе для instruction {es}')

        return False

    id_user = call.message.chat.id

    if user_system == 'iphone':
        file_video = r'src/telegram/media/iphone.MOV'
    elif user_system == 'android':
        file_video = r'src/telegram/media/android.MOV'
    elif user_system == 'pc':
        file_video = r'src/telegram/media/pc.MOV'

    # media = types.MediaGroup()
    # media.attach_video(types.InputFile(file_video), 'rb')

    await call.bot.send_chat_action(id_user, ChatActions.UPLOAD_VIDEO)

    # await call.bot.send_media_group(id_user, media=media)

    with open(file_video, 'rb') as file:

        import cv2
        file_path = file_video
        vid = cv2.VideoCapture(file_path)
        height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        height = int(height)
        width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        width = int(width)

        await call.bot.send_video(id_user, file, width=width, height=height)

    await start(call.message)


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

    dp.register_callback_query_handler(support, text='support')

    dp.register_callback_query_handler(instruction, text_contains='instruction-')
