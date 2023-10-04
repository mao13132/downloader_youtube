# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from aiogram import types

from settings import LOGO
from src.telegram.bot_core import BotDB
from src.telegram.keyboard.keyboards import Admin_keyb
from src.telegram.logic._mailing import _mailing

from src.telegram.sendler.sendler import Sendler_msg


async def good_mal(call: types.CallbackQuery):
    await Sendler_msg.log_client_call(call)

    id_user = call.message.chat.id

    try:
        await call.message.edit_caption(caption=f'Идёт рассылка...', reply_markup=None)
    except:
        try:
            await call.message.edit_text(text=f'Идёт рассылка...', reply_markup=None)
        except:
            pass

    try:

        _, id_pk = str(call.data).split('-')

    except Exception as es:

        print(f'Ошибка при разборе для good_mal {es}')

        return False

    row_sql_response = BotDB.get_response_word_from_id_pk(id_pk)

    users_list = BotDB.get_all_users()

    if users_list == []:
        await Sendler_msg.send_msg_call(call, f'⛔️ Список пользователей пуст', Admin_keyb().start_keyb(id_user))

        return False

    good_count_send = 0

    for _user in users_list:
        id_client = _user[1]

        res_send = await _mailing(call.message, id_client, row_sql_response)

        if res_send:
            good_count_send += 1

    keyb = Admin_keyb().admin_panel()

    await Sendler_msg().sendler_photo_call(call, LOGO, f'🍀 Рассылка {good_count_send} '
                                                             f'пользователям выполнена', keyb)

    return True
