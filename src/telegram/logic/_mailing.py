# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import asyncio
import random

from aiogram.types import Message, ChatActions

from src.telegram.logic.sendler_file import SenderFile

from src.telegram.sendler.sendler import Sendler_msg


async def _mailing(message, id_user, row_sql_response):
    _, _search_word, _type_msg, _text_msg, _patch_file, *_ = row_sql_response

    res_ = False

    if _type_msg == 'voice':

        res_ = await SenderFile.sender_voice(id_user, _patch_file, _text_msg)

    elif _type_msg == 'video_note':

        await message.bot.send_chat_action(id_user, ChatActions.RECORD_VIDEO_NOTE)

        res_ = await SenderFile.sender_video_note(id_user, _patch_file)

    elif _type_msg == 'text':

        await message.bot.send_chat_action(id_user, ChatActions.TYPING)

        res_ = await SenderFile.sender_text(id_user, _text_msg)

    elif _type_msg == 'video':
        await message.bot.send_chat_action(id_user, ChatActions.UPLOAD_VIDEO)

        res_ = await SenderFile.sender_video(id_user, _patch_file, _text_msg)

    elif _type_msg == 'photo':

        await message.bot.send_chat_action(id_user, ChatActions.UPLOAD_PHOTO)

        res_ = await SenderFile.sender_photo(id_user, _patch_file, _text_msg)

    else:

        await Sendler_msg.sendler_to_admin_mute(message,
                                                f'Не распознан тип контента send_response_word "{_type_msg}"', None)

    return res_
