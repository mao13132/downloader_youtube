# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import os
from datetime import datetime

from aiogram.types import Message
# from main import path_dir_project


async def download_photo_(message: Message):
    file_id = message.photo[-1].file_id

    file = await message.bot.get_file(file_id)

    file_path = file.file_path

    _sql_file_patch = os.path.join('media', f'{datetime.now().strftime("%H%M%S")}.jpg')

    await message.bot.download_file(file_path, _sql_file_patch)

    return _sql_file_patch
