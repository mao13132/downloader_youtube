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
import yt_dlp
from pytube import YouTube

from aiogram.types import ChatActions

from settings import dir_project
from src.telegram.sendler.sendler import Sendler_msg
from src.youtube.delete_file import delete_file

from src.telegram.bot_core import user_bot_core
import cv2


class DownloadVideo:
    filesize = 0

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

    async def new_video_download(self, result_dict):

        link = result_dict['link']

        id_user = result_dict['id_user']

        _filter = result_dict['filter']

        _dir = os.path.join(dir_project, 'down')

        ydl_opts = {
            'format': f'best[height<={_filter}]'
        }

        try:

            video = yt_dlp.YoutubeDL(ydl_opts)
            info_dict = video.extract_info(link, download=True)
            downloaded_file_path = video.prepare_filename(info_dict)
            video.close()

        except Exception as es:
            _error = (f'Ошибка при скачивание "{es}"')

            print(_error)

            result_dict['result'] = 'error'
            result_dict['error'] = _error

            return 'error'

        return downloaded_file_path

    async def get_video_no_1080(self, result_dict):

        link = result_dict['link']

        id_user = result_dict['id_user']

        _filter = result_dict['filter']

        _dir = os.path.join(dir_project, 'down')

        try:
            video_create = YouTube(link, use_oauth=True, allow_oauth_cache=True)
        except Exception as es:
            result_dict['result'] = 'error'
            result_dict['error'] = f"Ошибка при инициализации видео: {str(es)}"

            return 'error'

        list_stream = video_create.streams

        status_error = False

        for _try in range(len(list_stream)):

            try:
                if not status_error:
                    video_stream = video_create.streams.filter(res=f'{_filter}p').first()
                else:
                    video_stream = list_stream[_try]

                print(f'#{_try + 1} Начинаю обработку потока: {video_stream}')

                file_name_video = os.path.join(_dir, video_stream.default_filename)

                self.filesize = video_stream.filesize

                fn = video_stream.download(output_path=_dir)

                status_error = False

            except Exception as es:

                print(f'Ошибка при скачивание видео "{es}" Попытка "{_try}"')

                status_error = True

                continue

            if status_error:

                result_dict['result'] = 'error'
                result_dict['error'] = f"Попытка: '{_try}' video ошибка: '{str(es)}'"

                return 'error'

            else:

                return fn

    @staticmethod
    async def download_video(result_dict):

        filter = result_dict['filter']

        # if filter == '1080':
        #     result_dict['filter'] = 720

        # good_file = await DownloadVideo.get_video_and_audio_1080(result_dict)

        # good_file = await DownloadVideo().get_video_no_1080(result_dict)
        good_file = await DownloadVideo().new_video_download(result_dict)

        print(f'Скачал видео {good_file}')

        result_dict['result'] = good_file

        return True
