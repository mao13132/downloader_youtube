from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


class Call_admin:

    def admin(self):
        self._admin = CallbackData('adm', 'type', 'number', 'id')

        return self._admin


class Admin_keyb(Call_admin):
    def start_keyb(self):
        self._start_key = InlineKeyboardMarkup(row_width=1)

        self._start_key.add(InlineKeyboardButton(text=f'Скачать видео с Youtube', callback_data='youtube'))

        self._start_key.add(InlineKeyboardButton(text=f'Скачать звук с видео с YouTube', callback_data='mp3'))

        return self._start_key

    def youtube(self):
        self._start_key = InlineKeyboardMarkup(row_width=1)

        self._start_key.add(InlineKeyboardButton(text=f'🔙 Назад', callback_data='over_state'))

        return self._start_key

    def download_video(self):
        self._start_key = InlineKeyboardMarkup(row_width=4)

        self._start_key.insert(InlineKeyboardButton(text=f'360', callback_data='download-360'))

        self._start_key.insert(InlineKeyboardButton(text=f'480', callback_data='download-480'))

        self._start_key.insert(InlineKeyboardButton(text=f'720', callback_data='download-720'))

        self._start_key.insert(InlineKeyboardButton(text=f'1080', callback_data='download-1080'))

        self._start_key.add(InlineKeyboardButton(text=f'🔙 Назад', callback_data='over_state'))

        return self._start_key
