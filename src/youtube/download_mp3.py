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
from moviepy.editor import *

from settings import dir_project, LOGO
from src.telegram.keyboard.keyboards import Admin_keyb
from src.telegram.sendler.sendler import Sendler_msg
from src.youtube.delete_file import delete_file


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

            await Sendler_msg.sendler_admin_call(message, f'Ошибка при скачивания видео "{result_dict["link"]}" '
                                                          f'"{result_dict["error"]}"', None)

            try:
                await message.bot.delete_message(id_user, result_dict['one_msg_id'])
            except:
                pass

            return False

        video = open(result_dict['result'], 'rb')

        try:
            await message.bot.send_document(id_user, video)
        except Exception as es:

            delete_file(result_dict['result'])

            delete_file(result_dict['video'])

            if 'File too large for uploading. Check telegram api limit' in str(es):
                error = f'Размер видео превышает лимиты telegram по отправке файлов через ботов подробности ' \
                        f'https://core.telegram.org/bots/api#senddocument'

                error_user = f'Файл не может быть передан, слишком большой размер'

                print(error)

                try:
                    await message.bot.delete_message(id_user, result_dict['one_msg_id'])
                except:
                    pass

                await Sendler_msg().new_sendler_message(message, error_user, None)

                await Sendler_msg.sendler_admin_call(message, error, None)

                video.close()

                return False

            error = (f'Не могу выслать файл пользователю {id_user} "{es}"')

            print(error)

            await Sendler_msg.sendler_admin_call(message, error, None)

            video.close()

            return False

        video.close()

        try:
            await message.bot.delete_message(id_user, result_dict['one_msg_id'])
        except:
            pass

        over_msg = f'Надеюсь, я смог вам помочь 👉👈. Что-то еще?'

        keyb = Admin_keyb().start_keyb(id_user)

        await Sendler_msg().new_sendler_photo_message(message, LOGO, over_msg, keyb)

        delete_file(result_dict['result'])

        delete_file(result_dict['video'])

    @staticmethod
    def start_down(result_dict, test, _):
        asyncio.run(DownloadMp3.download_mp3(result_dict))

    @staticmethod
    async def download_mp3(result_dict):

        _filter = result_dict['filter']

        link = result_dict['link']

        _dir = os.path.join(dir_project, 'down')

        try:
            video = YouTube(link).streams.filter(res=f'{_filter}p').first().download(output_path=_dir)

            mp3_filename = video.split('.')[0]

            _mp3 = VideoFileClip(video)

            _mp3.audio.write_audiofile(os.path.join(_dir, f"{mp3_filename}.mp3"))

            _mp3.close()
        except Exception as es:

            result_dict['result'] = 'error'
            result_dict['error'] = str(es)

            return False

        result_dict['result'] = f'{mp3_filename}.mp3'

        result_dict['video'] = video

        return True
