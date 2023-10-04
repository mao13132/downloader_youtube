# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import asyncio
import os

from pytube import YouTube

from settings import dir_project, LOGO
from src.telegram.keyboard.keyboards import Admin_keyb
from src.telegram.sendler.sendler import Sendler_msg
from src.youtube.delete_file import delete_file


class DownloadVideo:
    @staticmethod
    async def wait_download(result_dict, call):
        while not result_dict['result']:
            await asyncio.sleep(3)

        if result_dict['result'] == 'error':

            if 'no attribute' in result_dict['error']:
                await Sendler_msg().new_sendler_message_call(call, f'У видео {result_dict["link"]} нет '
                                                                   f'{result_dict["filter"]}p.'
                                                                   f'Попробуйте выбрать другое качество', None)

            await Sendler_msg.sendler_admin_call(call, f'Ошибка при скачивания видео "{result_dict["link"]}" '
                                                       f'"{result_dict["error"]}"', None)

            return False

        id_user = call.message.chat.id

        video = open(result_dict['result'], 'rb')

        try:
            await call.bot.send_video(id_user, video)
        except Exception as es:

            delete_file(result_dict['result'])

            if 'File too large for uploading. Check telegram api limit' in str(es):
                error = f'У пользователя ID: {id_user} ошибка. Размер видео превышает лимиты telegram по отправке ' \
                        f'файлов через ботов подробности ' \
                        f'https://core.telegram.org/bots/api#senddocument'

                error_user = f'У пользователя ID: {id_user} ошибка. Файл не может быть передан, слишком большой размер'

                print(error)

                await Sendler_msg().new_sendler_message_call(call, error_user, None)

                await Sendler_msg.sendler_admin_call(call, error, None)

                video.close()

                return False

            error = (f'У пользователя ID: {id_user} ошибка. Не могу выслать файл пользователю {id_user} "{es}"')

            print(error)

            await Sendler_msg.sendler_admin_call(call, error, None)

            video.close()

            return False

        video.close()

        over_msg = f'Надеюсь, я смог вам помочь 👉👈. Что-то еще?'

        keyb = Admin_keyb().start_keyb(id_user)

        await Sendler_msg().new_sendler_photo_call(call, LOGO, over_msg, keyb)

        delete_file(result_dict['result'])

    @staticmethod
    def start_down(call, _filter, link, result_dict):
        asyncio.run(DownloadVideo.download_video(call, _filter, link, result_dict))

    @staticmethod
    async def download_video(call, _filter, link, result_dict):

        _dir = os.path.join(dir_project, 'down')

        try:
            fn = YouTube(link).streams.filter(res=f'{_filter}p').first().download(output_path=_dir)
        except Exception as es:

            result_dict['result'] = 'error'
            result_dict['error'] = str(es)

            return False

        result_dict['result'] = fn

        return True
