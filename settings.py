import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), 'src', 'telegram', '.env')

load_dotenv(dotenv_path)

ADMIN = ['331583382']

TOKEN = os.getenv('TOKEN')

LOGO = r'src/telegram/media/logo.jpg'

VIDEO_TYPE = ['360', '480', '720', '1080']

dir_project = os.getcwd()
