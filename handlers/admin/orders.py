from aiogram.types import Message
from loader import dp, db
from handlers.user.menu import orders
from filters import IsAdmin


@dp.message_handler(IsAdmin(), text=orders)
async def process_orders(message: Message):
    orders_list = db.fetchall('SELECT * FROM orders')

    if len(orders_list) == 0:
        await message.answer('У вас нема заказів.')
    else:
        await order_answer(message, orders_list)


async def order_answer(message, orders_list):
    res = ''

    for order in orders_list:
        res += f'Замолення <b>№{order[3]}</b>\n\n'

    await message.answer(res)
