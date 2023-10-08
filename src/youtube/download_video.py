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
import sys
import time

from pytube import YouTube

from aiogram.types import ChatActions

from settings import dir_project, LOGO, VIDEO_TYPE
from src.telegram.sendler.sendler import Sendler_msg
from src.youtube.delete_file import delete_file

from src.telegram.bot_core import user_bot_core
import cv2


# apt-get update && apt-get install libgl1

class DownloadVideo:
    filesize = 0
    """строке 223 файла innertube.py с ANDROID_MUSIC на ANDROID,
    и YouTube(link, use_oauth=False, allow_oauth_cache=True) """

    def progress_function(self, chunk, file_handle, bytes_remaining):
        global filesize
        current = ((filesize - bytes_remaining) / filesize)
        percent = ('{0:.1f}').format(current * 100)
        progress = int(50 * current)
        status = '█' * progress + '-' * (50 - progress)
        sys.stdout.write(' ↳ |{bar}| {percent}%\r'.format(bar=status, percent=percent))
        sys.stdout.flush()

    @staticmethod
    async def progress(current, total):
        print(f"{current * 100 / total:.1f}%")

    @staticmethod
    async def wait_download(result_dict, call):

        id_user = call.message.chat.id

        while not result_dict['result']:
            await asyncio.sleep(3)

        if result_dict['result'] == 'error':

            if 'no attribute' in result_dict['error']:
                await Sendler_msg().new_sendler_message_call(call, f'Пользователь: {id_user}\n'
                                                                   f'У видео {result_dict["link"]} нет '
                                                                   f'{result_dict["filter"]}p.'
                                                                   f'Попробуйте выбрать другое качество', None)

            await Sendler_msg.sendler_admin_call(call, f'Пользователь: {id_user}\n'
                                                       f'Ошибка при скачивания видео "{result_dict["link"]}" '
                                                       f'"{result_dict["error"]}"', None)

            return False

        id_user = call.message.chat.id

        file_path = result_dict['result']
        vid = cv2.VideoCapture(file_path)
        height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        height = int(height)
        width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        width = int(width)
        del vid

        video = open(result_dict['result'], 'rb')

        try:
            me = await call.bot.me

            await call.bot.send_chat_action(id_user, ChatActions.UPLOAD_VIDEO)

            await user_bot_core.app.send_video(f'@{me.username}', video, caption=id_user,
                                               progress=DownloadVideo.progress, width=width, height=height)


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

        delete_file(result_dict['result'])

    @staticmethod
    def start_down(call, _filter, link, result_dict):

        result = asyncio.run(DownloadVideo.download_video(result_dict))

        return True

    async def get_video_no_1080(self, result_dict):

        link = result_dict['link']

        id_user = result_dict['id_user']

        _filter = result_dict['filter']

        _dir = os.path.join(dir_project, 'down')

        file_name_video = ''

        for _try in range(6):

            try:
                video_create = YouTube(link, use_oauth=True, allow_oauth_cache=True)

                video_stream = video_create.streams.filter(res=f'{_filter}p').first()

                file_name_video = os.path.join(_dir, video_stream.default_filename)

                self.filesize = video_stream.filesize

                fn = video_stream.download(output_path=_dir)

            except Exception as es:

                if 'NoneType' in str(es):
                    index_filter = VIDEO_TYPE.index(str(_filter))

                    try:
                        _filter = VIDEO_TYPE[index_filter - 1]
                    except:
                        result_dict['result'] = 'error'
                        result_dict['error'] = f"Нет такого типа: {str(es)}"

                        return 'error'

                    continue

                if _try < 5:
                    print(f'Ошибка {str(es)} делаю попытку {_try + 1}')

                    time.sleep(60)

                    index_filter = VIDEO_TYPE.index(str(_filter))

                    try:
                        _filter = VIDEO_TYPE[index_filter - 1]
                    except:
                        pass

                    try:
                        delete_file(file_name_video)
                    except:
                        pass

                    continue

                result_dict['result'] = 'error'
                result_dict['error'] = f"Попытка: '{_try}' video ошибка: '{str(es)}'"

                return 'error'

            return fn

    @staticmethod
    async def download_video(result_dict):

        filter = result_dict['filter']

        if filter == '1080':
            result_dict['filter'] = 720

        # good_file = await DownloadVideo.get_video_and_audio_1080(result_dict)

        good_file = await DownloadVideo().get_video_no_1080(result_dict)

        print(f'Скачал видео {good_file}')

        result_dict['result'] = good_file

        return True
