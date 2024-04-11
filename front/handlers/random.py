from aiogram import types
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.command import Command
from aiogram import Router, F
from config_reader import config
from aiogram.utils.keyboard import InlineKeyboardBuilder
from funcs.const import *

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import logging


router = Router()


@router.message()
async def random(message: Message):
    await message.answer('Кажется, вы написали что-то рандомное.\n42\n/restart')