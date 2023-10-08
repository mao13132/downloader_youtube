# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import os

from src.sql.bd import BotDB

from src.telegram_user.tg_auth_module import TgAuthModule


path_dir_project = os.path.dirname(__file__)

sessions_path = os.path.join(path_dir_project, 'src', 'telegram_user', 'sessions')

user_bot_core = TgAuthModule(sessions_path, BotDB)
