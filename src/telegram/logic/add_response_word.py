# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------

from aiogram.types import Message

from src.telegram.logic.download_media.download_photo import download_photo_
from src.telegram.logic.download_media.download_video import download_video_
from src.telegram.logic.download_media.download_video_vote import download_video_vote
from src.telegram.logic.download_media.download_voice import download_voice_

from src.telegram.bot_core import BotDB


async def add_response_word(message: Message, search_word, tag=None):
    _type_msg = message.content_type

    if _type_msg == 'voice':
        _text_response = ''

        _sql_file_patch = await download_voice_(message)

    elif _type_msg == 'video_note':
        _text_response = message.caption if message.caption is not None else message.text

        _sql_file_patch = await download_video_vote(message)

    elif _type_msg == 'text':
        _text_response = message.text

        _sql_file_patch = ''

    elif _type_msg == 'video':
        _text_response = message.caption if message.caption is not None else message.text

        _sql_file_patch = await download_video_(message)

    elif _type_msg == 'photo':
        _text_response = message.caption if message.caption is not None else message.text

        _sql_file_patch = await download_photo_(message)
    else:
        _text_response = message.caption if message.caption is not None else message.text

        _sql_file_patch = ''

    id_pk = BotDB.add_response_msg(search_word, _type_msg, _sql_file_patch, _text_response, tag)

    return id_pk
