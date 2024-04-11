import json
import requests


from aiogram import Router, F, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from custom_filtrs.custom import Square_F
from funcs.const import *

from keyboards.simple_row import make_row_keyboard
from aiogram.utils.keyboard import InlineKeyboardBuilder


router = Router()



@router.message(StateFilter(None), F.text == catch_3)
async def cian_id(message: Message, state: FSMContext):

    text = '''Авторы: @jeydipak & @ChopperT0ny

Стек: Apache Airflow, Postgres, aiogram, CatBoost, FastAPI, JS

Всего записей в БД: >70000

Спасибо, что зашли сюда. На создание этого всего ушло очень много сил.

        🪵🪵🪵
   🪵🪵🪵🪵🪵
 🪵🪵🪵🪵🪵🪵
 🪵🧱🧱🧱🧱🧱
 🧱🧱🧱🧱🪟🪟
 🧱🚪🚪🧱🪟🪟
 🧱🚪🚪🧱🧱🧱
 🧱🚪🚪🧱🧱🧱
🪨🪨🪨🪨🪨🪨🪨


Так что выбираем?
'''



    keyboard = make_row_keyboard(catches[:-1])
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
            text="А это что..",
            callback_data="secret")
        )
    
    await message.answer(
        text=text,
        reply_markup=builder.as_markup()
    )
    
    await message.answer(
        text='Что выбираем?',
        reply_markup=keyboard
    )

@router.callback_query(F.data == "secret")
async def send_location(callback: types.CallbackQuery):

    await callback.message.answer_sticker(sticker='CAACAgQAAxkBAAEEnRxmFnvKC-C5hn8S6oOMZ0dB4T_51AACJQEAAqghIQbYv0ET_Pm8ejQE')
    await callback.message.delete()