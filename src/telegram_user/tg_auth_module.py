# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import asyncio
import time

from pyrogram import Client

from settings import *

from datetime import datetime


class TgAuthModule:
    def __init__(self, sessions_patch, BotDB):
        """@developer_telegrams"""
        self.BotDB = BotDB
        self.path = sessions_patch + f'/{API_ID}'
        self.ADMIN_SEND_SLEEP = 40
        self.ITER_CHAT_SLEEP = 60

    async def start_tg(self):

        print(f'{datetime.now().strftime("%H:%M:%S")} Инициализирую вход в аккаунт {API_ID}')

        try:
            self.app = Client(self.path, API_ID, API_HASH)

            await self.app.start()

        except Exception as es:
            print(f'{datetime.now().strftime("%H:%M:%S")} Ошибка при авторизации ({API_ID}) "{es}"')

            return False

        return self
