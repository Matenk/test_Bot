from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from key import api
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio



bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Расчет')
kb.add(button)

kb2 = InlineKeyboardMarkup()
button2 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button3 = InlineKeyboardButton(text='Формула расчета', callback_data='formulas')
kb2.add(button2)
kb2.add(button3)
class UserState(StatesGroup):

    age = State()
    growth = State()
    weight = State()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    print("Кнопка 'Рассчитать норму калорий' нажата")
    await call.message.answer('Введи свой возраст.')
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    if not message.text.isdigit() or not (
            0 < int(message.text) < 120):
        await message.answer('Пожалуйста, введите корректный возраст (число от 1 до 120).')
        return
    await state.update_data(age=message.text)
    await message.answer(f'Целых {message.text} лет...и как ты справляешься с такими высокими технологиями в твоем-то возрасте? Введи свой рост в см.')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    if not message.text.isdigit() or not (50 < int(message.text) < 300):
        await message.answer('Пожалуйста, введите корректный рост (число от 50 до 300 сантиметров).')
        return
    await state.update_data(growth=message.text)
    await message.answer('Введи свой вес в кг. Обещаю никому не скажу (нет).')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    if not message.text.isdigit() or not (20 < int(message.text) < 300):
        await message.answer('Пожалуйста, введите корректный вес (число от 20 до 300 кг).')
        return
    await state.update_data(weight=message.text)
    data = await state.get_data()
    w = data["weight"]
    g = data["growth"]
    a = data["age"]
    calories = 10 * int(w) + int(6.25) * int(g) - 5 * int(a) + 5
    await message.answer(f'Ууу, дорогуша, твоя суточная норма ккал: {calories}, крч столько сколько ты съела сегодня на завтрак...\n Пока!')
    await state.finish()








@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('(10 × вес в килограммах) + (6,25 × рост в сантиметрах) − (5 × возраст в годах) + 5')
    await call.answer()



@dp.message_handler(text='Расчет')
async def main_menu(message):
    await message.answer('Выбери опцию', reply_markup=kb2)



@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer('Привет, сладкая! Я бот помогающий твоему здоровью! Нажми Расчет, чтобы словить кринж', reply_markup=kb)


@dp.message_handler()
async def all_message(message):
    await message.answer('Введи команду /start чтобы начать общение!')




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

