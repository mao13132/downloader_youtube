import asyncio
import threading

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ChatActions
from pytube import YouTube

from _clear import _clear
from src.telegram.logic.checking_for_a_subscription import checking_for_a_subscription, check_group
from src.telegram.logic.devision_msg import division_message
from src.telegram.handlers.users import start
from src.telegram.logic.good_mal import good_mal
from src.telegram.sendler.sendler import *

from src.telegram.keyboard.keyboards import *
from src.telegram.state.states import States

from src.telegram.bot_core import BotDB

from src.youtube.download_video import DownloadVideo


async def over_state(call: types.CallbackQuery, state: FSMContext):

    subs = await checking_for_a_subscription(call.message)

    if not subs:
        return False

    await state.finish()

    id_user = call.message.chat.id

    user_name = call.message.chat.first_name if call.message.chat.first_name is not None else call.message.chat.username

    _msg = f'Здравствуйте {user_name}! Что вам требуется от бота?'

    keyb = Admin_keyb().start_keyb(id_user)

    await Sendler_msg().sendler_photo_call(call, LOGO, _msg, keyb)


async def youtube(call: types.CallbackQuery, state: FSMContext):

    subs = await checking_for_a_subscription(call.message)

    if not subs:
        return False

    _msg = f'Вставьте ссылку на видео с YouTube, чтобы получить видеофайл 🎥'

    keyb = Admin_keyb().youtube()

    await Sendler_msg().sendler_photo_call(call, LOGO, _msg, keyb)

    await States.add_link.set()


async def support(call: types.CallbackQuery, state: FSMContext):

    subs = await checking_for_a_subscription(call.message)

    if not subs:
        return False

    await call.bot.answer_callback_query(call.id)

    _msg = f'Какой телефон вы используете?'

    keyb = Admin_keyb().system()

    await Sendler_msg().sendler_photo_call(call, LOGO, _msg, keyb)


async def mp3(call: types.CallbackQuery, state: FSMContext):

    subs = await checking_for_a_subscription(call.message)

    if not subs:
        return False

    await call.bot.answer_callback_query(call.id)

    _msg = f'Вставьте ссылку на видео с YouTube для получения звука с видео'

    keyb = Admin_keyb().youtube()

    await Sendler_msg().sendler_photo_call(call, LOGO, _msg, keyb)

    await States.add_link_mp3.set()


async def download(call: types.CallbackQuery, state: FSMContext):

    subs = await checking_for_a_subscription(call.message)

    if not subs:
        return False

    await state.finish()

    await call.bot.answer_callback_query(call.id)

    try:

        _, _filter, id_pk = str(call.data).split('-')

    except Exception as es:

        print(f'Ошибка при разборе для download call{es}')

        return False

    id_user = call.message.chat.id

    login = call.message.chat.username if call.message.chat.username is not None else call.message.chat.first_name

    user_data = BotDB.get_user_data_from_id(id_user)

    down_status = user_data[8]

    if down_status != 0:
        error = (f'⚠️ {login}, пожалуйста, <b>дождитесь</b>, пока скачается предыдущее видео')
        print(error)

        await Sendler_msg().new_sendler_message_call(call, error, Admin_keyb().start_keyb(id_user))

        return False

    link = BotDB.get_link(id_pk)

    video = YouTube(link)

    name_file = f'down{os.sep}{video.title}'

    change_down_status = BotDB.update_user_key(id_user, 'down_status', 1)

    result_dict = {'result': False, 'filter': _filter, 'link': link, 'id_user': id_user, 'call': call,
                   'name_file': name_file, 'over': False}

    _msg = f'<b>Lizard качает ваше видео 🎬</b>\nЭто может занять от 10 секунд до 5 минут 🛜'

    one_msg = await Sendler_msg().sendler_photo_call(call, LOGO, _msg, None)

    result_dict['one_msg_id'] = one_msg.message_id

    trh = threading.Thread(target=DownloadVideo.start_down,
                           args=(call, _filter, link, result_dict),
                           name=(f'thr-{id_user}'))

    trh.start()

    wait_download = asyncio.create_task(DownloadVideo.wait_download(result_dict, call, BotDB))

    wait_download = asyncio.create_task(DownloadVideo.wait_over(result_dict, call))


async def admin_panel(call: types.CallbackQuery, state: FSMContext):
    await call.bot.answer_callback_query(call.id)

    id_user = call.message.chat.id

    await state.finish()

    await Sendler_msg.log_client_call(call)

    keyb = Admin_keyb().admin_panel()

    text_admin = 'Админ панель:'

    await Sendler_msg().sendler_photo_call(call, LOGO, text_admin, keyb)


async def clear(call: types.CallbackQuery):
    await call.bot.answer_callback_query(call.id)

    BotDB.refresh_status_all()

    id_user = call.message.chat.id

    await Sendler_msg.log_client_call(call)

    res_clear = await _clear()

    if res_clear:
        _msg = f'✅ Хранилище успешно очищено'
    else:
        _msg = f'⛔️ Не могу очистить хранилище'

    keyb = Admin_keyb().admin_panel()

    await Sendler_msg().sendler_photo_call(call, LOGO, _msg, keyb)


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

    _msg += '\n\n'.join(f"{count + 1}. Логин: {f'@{x[2]}' if x[2] is not None else 'Не указан'} ID: {x[1]} "
                        f"Скачал: {x[7]}"
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

    await call.bot.send_chat_action(id_user, ChatActions.UPLOAD_VIDEO)

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


async def menu_sub(call: types.CallbackQuery, state: FSMContext):
    await state.finish()

    await call.bot.answer_callback_query(call.id)

    id_user = call.message.chat.id

    sub_status = BotDB.get_subs_status()

    sub_id_channel = BotDB.get_id_subs_channel()

    sub_link_channel = BotDB.get_link_subs_channel()

    sub_count_down = BotDB.get_count_subs_file_down()

    await Sendler_msg.log_client_call(call)

    button_dict = {}

    if sub_status == '1':
        status = f'<b>✅ Включена</b>'
        button_dict['status_button'] = f'🅾️ Выключить'
        button_dict['status_button_call'] = 'subs-off'
    else:
        status = f'<b>🅾️ Выключена</b>'
        button_dict['status_button'] = f'✅ Включить'
        button_dict['status_button_call'] = 'subs-on'

    if sub_id_channel == '0':
        id_channel = '<b>Не указан</b>'
        button_dict['id_channel_button'] = f'🖋 Указать ID'
        button_dict['id_channel_button_call'] = 'set_id_channel'
    else:
        id_channel = sub_id_channel
        button_dict['id_channel_button'] = f'✏️ Изменить ID'
        button_dict['id_channel_button_call'] = 'set_id_channel'

    if sub_link_channel == '0':
        link_channel = '<b>Не указана</b>'
        button_dict['link_channel_button'] = f'🖋 Указать ссылку'
        button_dict['link_channel_button_call'] = 'set_link_channel'
    else:
        link_channel = sub_link_channel
        button_dict['link_channel_button'] = f'✏️ Изменить ссылку'
        button_dict['link_channel_button_call'] = 'set_link_channel'

    button_dict['count_down'] = f'✏️ Изменить кол-во'
    button_dict['count_down_call'] = 'set_count_down'

    _msg = f'Состояние: {status}\n\n' \
           f'ID источника: {id_channel}\n\n' \
           f'Пригласительная ссылка: {link_channel}\n\n' \
           f'Через сколько скачек подписывать: <b>{sub_count_down}</b>'

    keyb = Admin_keyb().subs_menu(button_dict)

    await Sendler_msg().sendler_photo_call(call, LOGO, _msg, keyb)


async def subs(call: types.CallbackQuery, state: FSMContext):
    await Sendler_msg.log_client_call(call)

    try:
        _, trigger = str(call.data).split('-')
    except:

        error = (f'⚠️ Ошибка при разборе subs')

        print(error)

        await Sendler_msg.send_msg_call(call, error, None)

        return False

    if trigger == 'on':
        status = 1
    else:
        status = 0

    BotDB.update_settings('subs', status)

    await menu_sub(call, state)


async def set_id_channel(call: types.CallbackQuery, state: FSMContext):
    await Sendler_msg.log_client_call(call)

    id_user = call.message.chat.id

    _msg = f'Отправьте мне следующим сообщение ID канала на который необходимо проверять подписку'

    keyb = Admin_keyb().back_subs()

    await Sendler_msg().sendler_photo_call(call, LOGO, _msg, keyb)

    await States.set_id.set()


async def set_link_channel(call: types.CallbackQuery, state: FSMContext):
    await Sendler_msg.log_client_call(call)

    id_user = call.message.chat.id

    _msg = f'Отправьте мне следующим сообщение пригласительную ссылку на канал на который необходимо подписываться'

    keyb = Admin_keyb().back_subs()

    await Sendler_msg().sendler_photo_call(call, LOGO, _msg, keyb)

    await States.set_link.set()


async def set_count_down(call: types.CallbackQuery, state: FSMContext):
    await Sendler_msg.log_client_call(call)

    id_user = call.message.chat.id

    _msg = f'Отправьте мне следующим сообщение кол-во скаченных файлов у пользователя после которого проверяю подписку'

    keyb = Admin_keyb().back_subs()

    await Sendler_msg().sendler_photo_call(call, LOGO, _msg, keyb)

    await States.set_count_down.set()


def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(youtube, text='youtube')

    dp.register_callback_query_handler(mp3, text='mp3')

    dp.register_callback_query_handler(over_state, text='over_state', state='*')

    dp.register_callback_query_handler(download, text_contains='download', state='*')

    dp.register_callback_query_handler(admin_panel, text_contains='admin_panel', state='*')

    dp.register_callback_query_handler(users, text_contains='users')

    dp.register_callback_query_handler(mailing_set, text='mailing_set')

    dp.register_callback_query_handler(good_mal, text_contains='good_mal-')

    dp.register_callback_query_handler(support, text='support')

    dp.register_callback_query_handler(instruction, text_contains='instruction-')

    dp.register_callback_query_handler(clear, text='clear')

    dp.register_callback_query_handler(menu_sub, text='menu_sub', state='*')

    dp.register_callback_query_handler(subs, text_contains='subs-')

    dp.register_callback_query_handler(set_id_channel, text='set_id_channel')

    dp.register_callback_query_handler(set_link_channel, text='set_link_channel')

    dp.register_callback_query_handler(set_count_down, text='set_count_down')

    dp.register_callback_query_handler(check_group, text='check_group')
