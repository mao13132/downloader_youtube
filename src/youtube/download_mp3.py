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
    async def wait_download(result_dict, message):

        id_user = message.chat.id

        while not result_dict['result']:
            await asyncio.sleep(3)

        if result_dict['result'] == 'error':

            if 'no attribute' in result_dict['error']:
                await Sendler_msg().new_sendler_message(message, f'У видео {result_dict["link"]} нет '
                                                                 f'{result_dict["filter"]}p.'
                                                                 f'Попробуйте выбрать другое качество', None)

            await Sendler_msg.sendler_admin_call(message, f'Ошибка при скачивания mp3 "{result_dict["link"]}" '
                                                          f'"{result_dict["error"]}"', None)

            await Sendler_msg().new_sendler_message(message, f'У видео {result_dict["link"]} проблемы с данным mp3, '
                                                             f'попробуйте другое', None)

            try:
                await message.bot.delete_message(id_user, result_dict['one_msg_id'])
            except:
                pass

            return False

        mp3 = open(result_dict['result'], 'rb')

        try:
            # await message.bot.send_document(id_user, mp3)

            me = await message.bot.me

            # await message.bot.send_chat_action(id_user, ChatActions.UPLOAD_AUDIO)

            await user_bot_core.app.send_audio(f'@{me.username}', mp3, caption=id_user)

        except Exception as es:

            delete_file(result_dict['result'])

            delete_file(result_dict['video'])

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

        delete_file(result_dict['result'])

        delete_file(result_dict['video'])

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

        _filter = result_dict['filter']

        _dir = os.path.join(dir_project, 'down')

        ydl_opts = {'extract_audio': True, 'format': 'bestaudio',
                    'outtmpl': f'{result_dict["name_file"]}.mp3'}

        try:

            video = yt_dlp.YoutubeDL(ydl_opts)
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

    # @staticmethod
    # async def download_mp3(result_dict):
    #
    #     _filter = result_dict['filter']
    #
    #     link = result_dict['link']
    #
    #     _dir = os.path.join(dir_project, 'down')
    #
    #     file_name_video = ''
    #
    #     for _try in range(6):
    #
    #         try:
    #             video_create = YouTube(link, use_oauth=True, allow_oauth_cache=True)
    #
    #             video_stream = video_create.streams.filter(res=f'{_filter}p', subtype='mp4').first()
    #
    #             video = video_stream.download(output_path=_dir)
    #
    #             # video = YouTube(link).streams.filter(res=f'{_filter}p').first().download(output_path=_dir)
    #
    #             file_name_video = os.path.join(_dir, video_stream.default_filename)
    #
    #             mp3_filename = video.split('.')[0]
    #
    #             _mp3 = VideoFileClip(video)
    #
    #             _mp3.audio.write_audiofile(os.path.join(_dir, f"{mp3_filename}.mp3"))
    #
    #             _mp3.close()
    #         except Exception as es:
    #
    #             if _try < 5:
    #                 print(f'Ошибка mp3 {str(es)} делаю попытку {_try + 1}')
    #
    #                 time.sleep(60)
    #
    #                 index_filter = VIDEO_TYPE.index(str(_filter))
    #
    #                 try:
    #                     _filter = VIDEO_TYPE[index_filter - 1]
    #                 except:
    #                     pass
    #
    #                 try:
    #
    #                     delete_file(file_name_video)
    #
    #                     delete_file(f'{mp3_filename}.mp3')
    #                 except:
    #                     pass
    #
    #                 continue
    #
    #             result_dict['result'] = 'error'
    #             result_dict['error'] = f'Попытка mp3  {str(es)}'
    #
    #             return False
    #
    #         result_dict['result'] = f'{mp3_filename}.mp3'
    #
    #         result_dict['video'] = video
    #
    #         return True
