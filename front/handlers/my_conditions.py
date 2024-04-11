import json
import requests


from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from custom_filtrs.custom import Square_F
from funcs.cian_m import gimi_smth
from funcs.geo_coder import coord_tg
from funcs.const import *

from keyboards.simple_row import make_row_keyboard

url_m = url + 'classify'


router = Router()


class CondState(StatesGroup):
    cond_1 = State()
    cond_2 = State()
    cond_3 = State()


@router.message(StateFilter(None), F.text == catch_1)
async def cian_id(message: Message, state: FSMContext):
    await message.answer(
        text="Укажите примерную площадь: ",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(CondState.cond_1)



@router.message(CondState.cond_1, Square_F())
async def cond_answer(message: Message, state: FSMContext):

    await state.update_data(square=message.text)

    await message.answer(
        text="Оцените качество ремонта: ",
        reply_markup=make_row_keyboard(available_quality_names)
    )
    await state.set_state(CondState.cond_2)



@router.message(CondState.cond_2, F.text.in_(available_quality_names))
async def cond_answer_2(message: Message, state: FSMContext):
    await state.update_data(quality=dict_qual[message.text])

    await message.answer(
        text="Кидай локацию: адрес или булавка 📍",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(CondState.cond_3)

@router.message(CondState.cond_3, F.location)
async def handle_location(message: Message, state: FSMContext):
    lat = message.location.latitude
    lan = message.location.longitude

    await state.update_data(lat=lat)
    await state.update_data(lan=lan)

    user_data = await state.get_data()
    
    forward = {
        'square': user_data['square'],
               'quality':user_data['quality'],
               'lat': user_data['lat'],
               'lan': user_data['lan'],
               }


    res = requests.post(url_m, json=forward)
    back = json.loads(res.content)

    price = back['classify_me']
    metro = back['metro_m']

    reply = f'''Справедливая стоимость данного объекта: {price}₽.
Станция метро: {metro}

Если хотие проверить ещё один объект, то введите площадь:

Вернуться назад:   /restart'''
    await message.answer(reply)
    await state.set_state(CondState.cond_1)



@router.message(CondState.cond_3)
async def cond_answer_3(message: Message, state: FSMContext):

    place = message.text

    if coord_tg(place) is None:
        reply = 'Введите адрес еще раз или нажмите /restart'
        await message.answer(reply)

    lat, lan = coord_tg(place)

    


    await message.answer_location(latitude = lat , longitude = lan)

    await state.update_data(lat=lat)
    await state.update_data(lan=lan)

    user_data = await state.get_data()
    
    forward = {
        'square': user_data['square'],
               'quality':user_data['quality'],
               'lat': user_data['lat'],
               'lan': user_data['lan'],
               }


    res = requests.post(url_m, json=forward)
    back = json.loads(res.content)

    price = back['classify_me']
    metro = back['metro_m']

    reply = f'''Справедливая стоимость данного объекта: {price}₽.
Станция метро: {metro}

Если хотие проверить ещё один объект, то введите площадь:

Вернуться назад:   /restart'''
    await message.answer(reply)
    await state.set_state(CondState.cond_1)




################################################################
@router.message(CondState.cond_1,)
async def food_chosen(message: Message, state: FSMContext):

    await message.answer(f'Введите площадь ещё раз или нажмите /restart')

@router.message(CondState.cond_2)
async def cond_answer_2(message: Message, state: FSMContext):

    await message.answer(
        text="Что-то пошло не так :(\nОцените качество ремонта или нажмите /restart:",
        reply_markup=make_row_keyboard(available_quality_names)
    )