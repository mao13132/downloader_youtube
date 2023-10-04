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

from src.telegram.logic.download_media.download_photo import download_photo_
from src.telegram.logic.download_media.download_video import download_video_
from src.telegram.logic.download_media.download_video_vote import download_video_vote
from src.telegram.logic.download_media.download_voice import download_voice_

from src.telegram.logic.sendler_file import SenderFile

from src.telegram.sendler.sendler import Sendler_msg


async def send_client_type_message(message, id_user, row_sql_response, keyb):
    _, _search_word, _type_msg, _text_msg, _patch_file, *_ = row_sql_response

    _text_msg = f'✅ Подтверждаете отправку сообщения клиенту?\n\n"{_text_msg}"'

    if _type_msg == 'voice':

        await SenderFile.sender_voice(id_user, _patch_file, _text_msg, keyb)

    elif _type_msg == 'video_note':

        await SenderFile.sender_video_note(id_user, _patch_file, keyb)

    elif _type_msg == 'text':

        await SenderFile.sender_text(id_user, _text_msg, keyb)

    elif _type_msg == 'video':

        await SenderFile.sender_video(id_user, _patch_file, _text_msg, keyb)

    elif _type_msg == 'photo':

        await SenderFile.sender_photo(id_user, _patch_file, _text_msg, keyb)

    else:

        await Sendler_msg.sendler_to_admin_mute(message,
                                                f'Не распознан тип контента send_response_word "{_type_msg}"', None)

    return True
