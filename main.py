import asyncio

from src.telegram.bot_core import *
from src.telegram.handlers.users import *
from src.telegram.state.states import *
from src.telegram.callbacks.call_user import *


def registration_all_handlers(dp):
    register_user(dp)

def registration_state(dp):
    register_state(dp)


def registration_calls(dp):
    register_callbacks(dp)


async def main():

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
