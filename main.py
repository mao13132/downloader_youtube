import asyncio

from _clear import _clear
from src.telegram.bot_core import *
from src.telegram.handlers.users import *
from src.telegram.state.states import *
from src.telegram.callbacks.call_user import *

from src.telegram.bot_core import user_bot_core

def registration_all_handlers(dp):
    register_user(dp)

def registration_state(dp):
    register_state(dp)


def registration_calls(dp):
    register_callbacks(dp)


async def main():

    await _clear()

    telegram_core = await user_bot_core.start_tg()

    if not telegram_core:
        return False

    print(f'Успешно авторизовался в user bote')

    bot_start = Core()

    registration_state(bot_start.dp)
    registration_all_handlers(bot_start.dp)
    registration_calls(bot_start.dp)

    try:
        await bot_start.dp.start_polling()
    finally:
        await bot_start.dp.storage.close()
        await bot_start.dp.storage.wait_closed()
        await bot_start.bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print(f'Бот остановлен!')
