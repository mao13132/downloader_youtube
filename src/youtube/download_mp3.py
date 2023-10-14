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
import time
import yt_dlp

from pytube import YouTube
from moviepy.editor import *
from aiogram.types import ChatActions

from settings import dir_project, LOGO, VIDEO_TYPE
from src.telegram.keyboard.keyboards import Admin_keyb
from src.telegram.sendler.sendler import Sendler_msg
from src.youtube.delete_file import delete_file
from src.telegram.bot_core import user_bot_core


class DownloadMp3:
    @staticmethod
    async def wait_download(result_dict, message, BotDB):

        id_user = message.chat.id

        while not result_dict['result']:
            await asyncio.sleep(3)

        change_down_status = BotDB.update_user_key(id_user, 'down_status', 0)

        if result_dict['result'] == 'error':

            try:
                await message.bot.delete_message(id_user, result_dict['one_msg_id'])
            except:
                pass

            if result_dict['error'] == 'big':
                await Sendler_msg().new_sendler_message_call(message, f'Ваш mp3 файл весит больше 2-х гигабайт. '
                                                                      f'Пожалуйста, укажите ссылку на другое видео 🫶',
                                                             None)

                return False

            if 'no attribute' in str(result_dict['error']):
                await Sendler_msg().new_sendler_message(message, f'У видео {result_dict["link"]} нет '
                                                                 f'{result_dict["filter"]}p.'
                                                                 f'Попробуйте выбрать другое качество', None)

            await Sendler_msg.sendler_admin_call(message, f'Ошибка при скачивания mp3 "{result_dict["link"]}" '
                                                          f'"{result_dict["error"]}"', None)

            await Sendler_msg().new_sendler_message(message, f'У видео {result_dict["link"]} проблемы с данным mp3, '
                                                             f'попробуйте другое', None)

            return False

        mp3 = open(result_dict['result'], 'rb')

        try:

            me = await message.bot.me

            await user_bot_core.app.send_audio(f'@{me.username}', mp3, caption=id_user)

            try:
                await message.bot.delete_message(id_user, result_dict['one_msg_id'])
            except:
                pass

            BotDB.plus_count_down(id_user)

        except Exception as es:
            try:
                delete_file(result_dict['result'])

                delete_file(result_dict['video'])
            except:
                pass

            if 'File too large for uploading. Check telegram api limit' in str(es):
                error = f'Размер видео превышает лимиты telegram по отправке файлов через ботов подробности ' \
                        f'https://core.telegram.org/bots/api#senddocument'

                error_user = f'Файл не может быть передан, слишком большой размер mp3'

                print(error)

                try:
                    await message.bot.delete_message(id_user, result_dict['one_msg_id'])
                except:
                    pass

                await Sendler_msg().new_sendler_message(message, error_user, None)

                await Sendler_msg.sendler_admin_call(message, error, None)

                mp3.close()

                return False

            error = (f'Не могу выслать файл пользователю {id_user} "{es}"')

            print(error)

            await Sendler_msg.sendler_admin_call(message, error, None)

            mp3.close()

            return False

        mp3.close()

        try:
            await message.bot.delete_message(id_user, result_dict['one_msg_id'])
        except:
            pass

        try:

            delete_file(result_dict['result'])
        except:
            pass

    @staticmethod
    def start_down(result_dict, test, _):
        # result = asyncio.run(DownloadMp3.download_mp3(result_dict))
        result = asyncio.run(DownloadMp3.new_download_mp3(result_dict))

        return True

    @staticmethod
    async def new_download_mp3(result_dict):

        mp3_file = await DownloadMp3._new_download_mp3(result_dict)

        print(f'Скачал mp3 {mp3_file}')

        result_dict['result'] = mp3_file

        return True

    @staticmethod
    async def _new_download_mp3(result_dict):

        link = result_dict['link']

        id_user = result_dict['id_user']

        message = result_dict['message']

        _filter = result_dict['filter']

        _dir = os.path.join(dir_project, 'down')

        ydl_opts = {'extract_audio': True, 'format': 'bestaudio',
                    'outtmpl': f'{result_dict["name_file"]}.mp3'}

        try:

            video = yt_dlp.YoutubeDL(ydl_opts)

            info_dict = video.extract_info(link, download=False)

            file_size = info_dict['filesize'] if info_dict['filesize'] is not None else info_dict['filesize_approx']

            if file_size > 2048000000:
                result_dict['result'] = 'error'
                result_dict['error'] = f'big'

                return 'error'

            info_dict = video.extract_info(link, download=True)
            downloaded_file_path = video.prepare_filename(info_dict)
            video.close()

        except Exception as es:
            _error = (f'Ошибка при скачивание mp3 "{es}"')

            print(_error)

            result_dict['result'] = 'error'
            result_dict['error'] = _error

            return 'error'

        return downloaded_file_path
