from aiogram import types
from aiogram.types import Message
from datetime import datetime
from settings import *


class Sendler_msg:
    async def sendler_to_admin_mute(message: Message, text, keyb):
        for admin in ADMIN:
            try:
                await message.bot.send_message(int(admin), text, reply_markup=keyb, disable_notification=True)
            except:
                try:
                    await message.bot.send_message(int(admin), text)
                except Exception as es:
                    if str(es) == 'Chat not found':
                        print(f'Бот не имеет права писать админу, напишите /start боту')
                    else:
                        print(f'Ошибка при отправке сообщение админу текст: "{text}" {es}')

    async def sendler_to_admin(message: Message, text, keyb):
        for admin in ADMIN:
            try:
                await message.bot.send_message(int(admin), text, reply_markup=keyb)
            except:
                try:
                    await message.bot.send_message(int(admin), text)
                except Exception as es:
                    if str(es) == 'Chat not found':
                        print(f'Бот не имеет права писать админу, напишите /start боту')
                    else:
                        print(f'Ошибка при отправке сообщение админу текст: "{text}" {es}')

    async def sendler_admin_call(call: types.CallbackQuery, text, keyb):
        for admin in ADMIN:
            try:
                await call.bot.send_message(int(admin), text, reply_markup=keyb, disable_web_page_preview=True)
            except:
                try:
                    await call.bot.send_message(int(admin), text, disable_web_page_preview=True)
                except Exception as es:
                    if str(es) == 'Chat not found':
                        print(f'Бот не имеет права писать админу {admin}, напишите /start боту')
                    else:
                        print(f'Ошибка при отправке сообщение админу текст {admin},: "{text}" {es}')

    async def send_msg_call(call: types.CallbackQuery, text_msg, keyb):
        try:
            await call.message.edit_caption(caption=text_msg, reply_markup=keyb)
        except Exception as es:
            # print(f'Ошибка редактирования поста: {es}')
            try:
                with open(LOGO, 'rb') as file:
                    await call.message.bot.send_photo(call.message.chat.id, file, caption=(text_msg),
                                                      reply_markup=keyb)
            except:
                try:
                    await call.message.bot.send_message(call.message.chat.id, text_msg,
                                                        reply_markup=keyb)

                except Exception as es:
                    print(f'Произошла ошибка при отправке поста текст: "{text_msg}" ошибка: "{es}"')
                    return False

        return True

    async def send_msg_message(message: Message, text_msg, keyb):
        if message.photo != []:

            try:
                await message.bot.send_message(message.chat.id, text_msg,
                                               reply_markup=keyb)
            except:
                print(f'Произошла ошибка при отправке поста текст: "{text_msg}" ошибка: "')
                return False
        else:
            try:
                await message.edit_text(text=text_msg, reply_markup=keyb)
            except:
                try:
                    await message.edit_caption(caption=text_msg, reply_markup=keyb)
                except:
                    try:
                        await message.bot.send_message(message.chat.id, text_msg,
                                                       reply_markup=keyb)
                    except Exception as es:
                        print(f'Произошла ошибка при отправке поста текст2: "{text_msg}" ошибка: {es}"')
                        return False

        return True

    async def send_call_message(call: types.CallbackQuery, text_msg, keyb):
        if call.message.photo != []:

            try:
                await call.message.bot.send_message(call.message.chat.id, text_msg,
                                                    reply_markup=keyb)
            except:
                print(f'Произошла ошибка при отправке поста текст: "{text_msg}" send_call_message"')
                return False
        else:
            try:
                await call.message.edit_text(text=text_msg, reply_markup=keyb)
            except:
                try:
                    await call.message.edit_caption(caption=text_msg, reply_markup=keyb)
                except Exception as es:
                    try:
                        await call.message.bot.send_message(call.message.chat.id, text_msg,
                                                            reply_markup=keyb)
                    except:
                        print(f'Произошла ошибка при отправке поста текст: "{text_msg}" send_call_message2 {es}"')
                        return False

        return True

    async def reply_user(message: Message, text_msg):

        try:
            await message.reply(text_msg)

        except Exception as es:
            print(f'Произошла ошибка при reply_user текст: "{text_msg}" ошибка: "{es}"')
            return False

        return True

    async def log_client_call(call: types.CallbackQuery):

        print()
        print(f'{str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))} '
              f'"{call.message.chat.full_name}" Кликает по кнопке "{call.data}"')
        print()
        try:
            await call.bot.answer_callback_query(call.id)
        except Exception as es:
            print(f'Уведомление: {es}')

    async def log_client_message(message: Message):

        print()
        print(f'{str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))} '
              f'"{message.chat.full_name}" написал "{message.text}"')
        print()

    async def sendler_photo_call(self, call, photo, text, keyb):
        try:
            with open(photo, 'rb') as file:
                file_photo = types.InputMediaPhoto(file)

                await call.message.edit_media(media=file_photo)
                await call.message.edit_caption(caption=text, reply_markup=keyb)
        except:
            try:
                with open(photo, 'rb') as file:
                    await call.message.bot.send_photo(call.message.chat.id, file, caption=(text),
                                                      reply_markup=keyb)
            except Exception as es:
                print(f'Ошибка при отправке сообщения call с фото {es}')
                return False

        return True

    async def new_sendler_photo_call(self, call, photo, text, keyb):

        try:
            with open(photo, 'rb') as file:
                await call.message.bot.send_photo(call.message.chat.id, file, caption=(text),
                                                  reply_markup=keyb)
        except Exception as es:
            print(f'Ошибка при отправке сообщения new_sendler_photo_call с фото {es}')
            return False

        return True

    async def sendler_photo_call_html(self, call, photo, text, keyb):
        try:
            with open(photo, 'rb') as file:
                file_photo = types.InputMediaPhoto(file)

                await call.message.edit_media(media=file_photo)
                await call.message.edit_caption(caption=text, reply_markup=keyb,)
        except:
            try:
                with open(photo, 'rb') as file:
                    await call.message.bot.send_photo(call.message.chat.id, file, caption=text,
                                                      reply_markup=keyb)
            except Exception as es:
                print(f'Ошибка при отправке сообщения call с фото {es}')
                return False

        return True

    async def sendler_photo_message(self, message, photo, text, keyb):
        try:
            with open(photo, 'rb') as file:
                file_photo = types.InputMediaPhoto(file)

                await message.edit_media(media=file_photo)
                await message.edit_caption(caption=text, reply_markup=keyb)
        except:
            try:
                with open(photo, 'rb') as file:
                    await message.bot.send_photo(message.chat.id, file, caption=(text),
                                                 reply_markup=keyb)
            except Exception as es:
                print(f'Ошибка при отправке сообщение msg с фото {es}')
                return False

        return True

    async def new_sendler_photo_message(self, message, photo, text, keyb):

        try:
            with open(photo, 'rb') as file:
                await message.bot.send_photo(message.chat.id, file, caption=(text),
                                             reply_markup=keyb)
        except Exception as es:
            print(f'Ошибка при отправке сообщение new_sendler_photo_message с фото {es}')
            return False

        return True
