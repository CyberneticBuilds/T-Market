import os
import handlers
from aiogram import executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from data import config
from loader import dp, db, bot
import filters
import logging

filters.setup(dp)

WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.environ.get("PORT", 5000))
user_message = 'Користувач'
admin_message = 'Адмін'


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row(user_message, admin_message)

    await message.answer('''Загальний привіт, хто не скине бабки на крипто, тому я яйця викручу як лампочку 
    ''', reply_markup=markup)


@dp.message_handler(text=user_message)
async def user_mode(message: types.Message):
    cid = message.chat.id
    if cid in config.ADMINS:
        config.ADMINS.remove(cid)

    await message.answer('Активовано режим підераса', reply_markup=ReplyKeyboardRemove())

    menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    menu_button = KeyboardButton('/menu')
    menu_keyboard.add(menu_button)

    # Optionally, send a follow-up message with the keyboard. This can be an informative message or even a blank message if you prefer.
    await message.answer("Тикни кнопку :", reply_markup=menu_keyboard)


@dp.message_handler(text=admin_message)
async def admin_mode(message: types.Message):
    cid = message.chat.id
    if cid not in config.ADMINS:
        config.ADMINS.append(cid)

    await message.answer('Активовано  режим режим боса', reply_markup=ReplyKeyboardRemove())

    menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    menu_button = KeyboardButton('/menu')
    menu_keyboard.add(menu_button)

    # Optionally, send a follow-up message with the keyboard. This can be an informative message or even a blank message if you prefer.
    await message.answer("Тикни кнопку :", reply_markup=menu_keyboard)

@dp.message_handler(lambda message: message.text and message.text.lower() == "button")
async def button_pressed(message: types.Message):
    # Here, treat the button press as if the user sent "/menu"
    # You can call the same function that handles the /menu command or directly place the code here
    await '/menu'

async def on_startup(dp):
    logging.basicConfig(level=logging.INFO)
    db.create_tables()

    await bot.delete_webhook()
    await bot.set_webhook(config.WEBHOOK_URL)


async def on_shutdown():
    logging.warning("Shutting down..")
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning("Bot down")


if __name__ == '__main__':

    if "HEROKU" in list(os.environ.keys()):

        executor.start_webhook(
            dispatcher=dp,
            webhook_path=config.WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT,
        )

    else:

        executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
