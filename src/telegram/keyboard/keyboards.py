from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from settings import ADMIN


class Call_admin:

    def admin(self):
        self._admin = CallbackData('adm', 'type', 'number', 'id')

        return self._admin


class Admin_keyb(Call_admin):
    def start_keyb(self, user_id):
        self._start_key = InlineKeyboardMarkup(row_width=1)

        self._start_key.add(InlineKeyboardButton(text=f'Скачать видео с Youtube', callback_data='youtube'))

        self._start_key.add(InlineKeyboardButton(text=f'Скачать звук с видео с YouTube', callback_data='mp3'))

        self._start_key.add(InlineKeyboardButton(text=f'Как пользоваться ботом?', callback_data='support'))

        if str(user_id) in ADMIN:
            self._start_key.add(InlineKeyboardButton(text=f'👨‍💻 Админ панель', callback_data='admin_panel'))

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

    def admin_panel(self):
        self._start_key = InlineKeyboardMarkup(row_width=1)

        self._start_key.add(InlineKeyboardButton(text=f'💵 Пользователи', callback_data='users'))

        self._start_key.add(InlineKeyboardButton(text=f'📩 Рассылка', callback_data='mailing_set'))

        self._start_key.add(InlineKeyboardButton(text=f'🔙 Назад', callback_data='over_state'))

        return self._start_key

    def send_client(self):
        self._start_key = InlineKeyboardMarkup(row_width=1)

        self._start_key.add(InlineKeyboardButton(text=f'🔙 Назад', callback_data=f'admin_panel'))

        return self._start_key

    def approve_mailing_set(self, id_pk):
        self._start_key = InlineKeyboardMarkup(row_width=1)

        self._start_key.add(InlineKeyboardButton(text=f'✅ Отправить', callback_data=f'good_mal-{id_pk}'))

        self._start_key.add(InlineKeyboardButton(text=f'❌ Отмена', callback_data=f'over_state'))

        return self._start_key

    def admin_back(self):
        self._start_key = InlineKeyboardMarkup(row_width=1)

        self._start_key.add(InlineKeyboardButton(text=f'🔙 Назад', callback_data='admin_panel'))

        return self._start_key

    def system(self):
        self._start_key = InlineKeyboardMarkup(row_width=1)

        self._start_key.add(InlineKeyboardButton(text=f'Айфон', callback_data=f'instruction-iphone'))

        self._start_key.add(InlineKeyboardButton(text=f'Андроид', callback_data=f'instruction-android'))

        self._start_key.add(InlineKeyboardButton(text=f'Компьютер', callback_data=f'instruction-pc'))

        self._start_key.add(InlineKeyboardButton(text=f'🔙 Назад', callback_data='over_state'))

        return self._start_key
