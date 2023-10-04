# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from ..bot_core import bot


class SenderFile:

    @staticmethod
    async def sender_voice(id_user, _patch_file, _text_msg, keyb=None):
        try:
            with open(_patch_file, 'rb') as file:
                await bot.send_voice(id_user, file, caption=_text_msg, reply_markup=keyb)
        except Exception as es:
            print(f'Ошибка send_voice {es}')

            return False

        return True

    @staticmethod
    async def sender_video_note(id_user, _patch_file, keyb=None):
        try:
            with open(_patch_file, 'rb') as file:
                await bot.send_video_note(id_user, file, reply_markup=keyb)
        except Exception as es:
            print(f'Ошибка sender_video_note {es}')

            return False

        return True

    @staticmethod
    async def sender_video(id_user, _patch_file, _text_msg, keyb=None):
        try:
            with open(_patch_file, 'rb') as file:
                await bot.send_video(id_user, file, caption=_text_msg, reply_markup=keyb)
        except Exception as es:
            print(f'Ошибка sender_video {es}')

            return False

        return True

    @staticmethod
    async def sender_photo(id_user, _patch_file, _text_msg, keyb=None):
        try:
            with open(_patch_file, 'rb') as file:
                await bot.send_photo(id_user, file, caption=_text_msg, reply_markup=keyb)
        except Exception as es:
            print(f'Ошибка sender_photo {es}')

            return False

        return True

    @staticmethod
    async def sender_text(id_user, _text_msg, keyb=None):
        try:
            await bot.send_message(id_user, _text_msg, reply_markup=keyb)
        except Exception as es:
            print(f'Ошибка sender_text {es}')

            return False

        return True
