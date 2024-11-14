from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from module_13_3 import UserState
import keybords as kb

router = Router()


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет, я бот помогающий твоему здоровью", reply_markup=kb.keyboard)


@router.message(F.text == 'Рассчитать')
async def main_menu(message: Message):
    await message.answer('Выберите действие', reply_markup=kb.keyboard2)


@router.callback_query(F.data == 'formulas')
async def get_formulas(callback: CallbackQuery):
    await callback.answer('Вы выбрали опцию',show_alert=True)
    await callback.message.answer(
        'Формула расчета калорийности: 88.362 + (13.397 * weight) + (4.799 * growth) - (5.677 * age)')


@router.callback_query(F.data == 'calories')
async def set_age(callback: CallbackQuery, state=FSMContext):
    await state.set_state(UserState.age)
    await callback.answer('Вы выбрали опцию',show_alert=True)
    await callback.message.answer('Введите ваш возраст')


@router.message(UserState.age)
async def get_growth(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(UserState.growth)
    await message.answer('Введите свой рост:')


@router.message(UserState.growth)
async def get_weight(message: Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await state.set_state(UserState.weight)
    await message.answer('Введите свой вес:')


@router.message(UserState.weight)
async def send_calories(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])
    calories = 88.362 + (13.397 * weight) + (4.799 * growth) - (5.677 * age)

    await message.answer(f'Ваша норма калорий:{calories} ')
    await state.clear()


@router.message()
async def all_message(message: Message):
    await message.answer('Нажмите команду /start, чтобы начать общение')
