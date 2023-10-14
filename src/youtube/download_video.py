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

from settings import dir_project, LOGO
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
    async def wait_download(result_dict, call, BotDB):

        id_user = call.message.chat.id

        while not result_dict['result']:
            await asyncio.sleep(3)

        change_down_status = BotDB.update_user_key(id_user, 'down_status', 0)

        if result_dict['result'] == 'error':

            try:
                await call.message.bot.delete_message(id_user, result_dict['one_msg_id'])
            except:
                pass

            if result_dict['error'] == 'big':
                await Sendler_msg().new_sendler_message_call(call, f'Ваше видео весит больше 2-х гигабайт. '
                                                                   f'Пожалуйста, вставьте еще раз эту же ссылку '
                                                                   f'и выберите качество меньше 🫶', None)

                return False

            if 'no attribute' in str(result_dict['error']):
                await Sendler_msg().new_sendler_message_call(call, f'У видео {result_dict["link"]} нет '
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

            try:
                await call.message.bot.delete_message(id_user, result_dict['one_msg_id'])
            except:
                pass

            BotDB.plus_count_down(id_user)

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

    @staticmethod
    async def download_video(result_dict):

        good_file = await DownloadVideo().new_video_download(result_dict)

        print(f'Скачал видео {good_file}')

        result_dict['result'] = good_file

        return True

    async def new_video_download(self, result_dict):

        _error = False

        link = result_dict['link']

        id_user = result_dict['id_user']

        call = result_dict['call']

        _filter = result_dict['filter']

        _dir = os.path.join(dir_project, 'down')

        ydl_opts = {
            'format': f'best[height<={_filter}]',
            'outtmpl': f'{result_dict["name_file"]}.mp4'
        }

        for _try in range(3):

            try:
                if _try > 1:
                    ydl_opts = {
                        'format': f'bestvideo+bestaudio/best',
                        'outtmpl': f'{result_dict["name_file"]}.mp4'
                    }

                video = yt_dlp.YoutubeDL(ydl_opts)

                info_dict = video.extract_info(link, download=False)

                file_size = info_dict['filesize'] if info_dict['filesize'] is not None else info_dict['filesize_approx']

                if file_size > 2048000000:
                    result_dict['result'] = 'error'
                    result_dict['error'] = f'big'

                    return 'error'

                print(f'Размер файла: {file_size}')

                info_dict = video.extract_info(link, download=True)

                downloaded_file_path = video.prepare_filename(info_dict)

                video.close()

                _error = False

                return downloaded_file_path

            except Exception as es:
                _error = (f'Ошибка при скачивание "{es}"')

                print(_error)

                _error = True

                time.sleep(10)

                continue

        if _error:
            result_dict['result'] = 'error'
            result_dict['error'] = _error

            return 'error'
