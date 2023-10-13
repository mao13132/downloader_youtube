import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), 'src', 'telegram', '.env')

load_dotenv(dotenv_path)

ADMIN = ['1422194909', '802664278']

TOKEN = os.getenv('TOKEN')

LOGO = r'src/telegram/media/logo.jpg'

VIDEO_TYPE = ['360', '480', '720', '1080']

VIDEO_TYPE_ANTI_BAG = ['144', '240', '360', '480', '720', '1080']

dir_project = os.getcwd()

########SETTINGS USERBOT########

USER_BOT_NAME = '@psihologhis'
# USER_BOT_NAME = '@YoutubeLizzard'

API_ID = 21480941  # API ID от аккаунта-userbot
# API_ID = 28172599  # API ID от аккаунта-userbot

API_HASH = '17e64dbfdc2a04c84f27baad5e311436'  # API hash от аккаунта-userbot
# API_HASH = 'f732a65a3851b0f75b4b71e546487a54'  # API hash от аккаунта-userbot
