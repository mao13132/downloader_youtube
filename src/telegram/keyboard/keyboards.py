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

    def download_video(self, id_pk, good_type):
        self._start_key = InlineKeyboardMarkup(row_width=4)

        for _type in good_type:
            self._start_key.insert(InlineKeyboardButton(text=_type, callback_data=f'download-{_type}-{id_pk}'))

        self._start_key.add(InlineKeyboardButton(text=f'🔙 Назад', callback_data='over_state'))

        return self._start_key
