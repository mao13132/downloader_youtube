from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from src.telegram.sendler.sendler import *

from src.telegram.keyboard.keyboards import *
from src.telegram.state.states import States


async def over_state(call: types.CallbackQuery, state: FSMContext):
    await state.finish()

    user_name = call.message.chat.first_name if call.message.chat.first_name is not None else call.message.chat.username

    _msg = f'Здравствуйте {user_name}! Что вам требуется от бота?'

    keyb = Admin_keyb().start_keyb()

    await Sendler_msg().sendler_photo_call(call, LOGO, _msg, keyb)


async def youtube(call: types.CallbackQuery, state: FSMContext):
    _msg = f'Вставьте ссылку на видео с YouTube'

    keyb = Admin_keyb().youtube()

    await Sendler_msg().sendler_photo_call(call, LOGO, _msg, keyb)

    await States.add_link.set()


async def download(call: types.CallbackQuery, state: FSMContext):
    await state.finish()

    try:

        _, _filter = str(call.data).split('-')

    except Exception as es:

        print(f'Ошибка при разборе для download call{es}')

        return False

    print()


def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(youtube, text='youtube')

    dp.register_callback_query_handler(over_state, text='over_state', state='*')

    dp.register_callback_query_handler(download, text_contains='download', state='*')
