from aiogram import types, Router, Dispatcher,F, Bot
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, callback_query
from db import get_user_info, add_user, get_specialities, check_user, update_user_info, get_specialities_for_reg, get_speciality_name_for_reg
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboard import make_spec_keyboard_for_reg, main_menu, edit_keybaoard
from other import get_joke
from config import bot


# Обработчик команды /start
router = Router()

class Reg(StatesGroup):
    user_id = State()
    first_name = State()
    last_name = State()
    speciality = State()
#Обработка инлайн-кнопки регистрация
@router.callback_query(F.data == "registration")#(Command('registration'))#(F.text == 'Регистрация')
async def reg_one(message: Message, state: FSMContext):
    await state.set_state(Reg.first_name)
    await bot.send_message(chat_id= message.from_user.id, text = 'Введи имя', reply_markup=types.ReplyKeyboardRemove())

@router.message(Reg.first_name)
async def reg_two(message: Message, state: FSMContext):
    await state.update_data(first_name= message.text)
    await state.set_state(Reg.last_name)
    await state.update_data(user_id = message.from_user.id)
    first_name1 = await state.get_data()
    await message.answer(f"Введи фамилию, {first_name1['first_name']}")

@router.message(Reg.last_name)
async def reg_three(message: Message, state: FSMContext):
    await state.update_data(last_name = message.text)
    await state.set_state(Reg.speciality)
    await message.answer("Интересно, а чем ты занимаешься в компании?", reply_markup=make_spec_keyboard_for_reg(get_specialities()))

@router.callback_query(Reg.speciality)
async def process_callback(callback: types.CallbackQuery, state: FSMContext):
    # Получаем callback_data
    speciality_id = callback.data.replace('spec_','')
    # Здесь вы можете обработать полученный ID специальности
    # Например, сохранить его в состояние пользователя
    await state.update_data(speciality_id=speciality_id)
    user_data = await state.get_data()
    joke = await get_joke(int(user_data['speciality_id']))
    spec_id = user_data['speciality_id']
    spec = get_speciality_name_for_reg(spec_id)
    spec_name = spec[0][1]
    if speciality_id ==12:
        message_spec = "В списке не нашлось для тебя подходящего. Мы разберемся и добавим."
    else:
        message_spec = spec_name
    if check_user(callback.from_user.id):
        update_user_info(user_data['user_id'],user_data['first_name'], user_data['last_name'], user_data['speciality_id'])
        await edit_keybaoard(callback,main_menu(),f"Я не знаю изменилось ли что-то, но тебе виднее.\n Имя, фамилия: {user_data['first_name']} {user_data['last_name']}\n Направление: {message_spec} \n _{joke}_")
    else:
        add_user(user_data['user_id'],user_data['first_name'], user_data['last_name'], user_data['speciality_id'])
        await edit_keybaoard(callback,main_menu(),f"Приятно познакомится. Давай сверим данные\n Имя, фамилия: {user_data['first_name']} {user_data['last_name']}\n Направление: {message_spec} \n*Если что-то неправильно, можешь изменить данные выполнив команду \start* \n _{joke}_")
    # Отправляем ответ пользователю
    #await callback.message.answer(text= f"Приятно познакомится, {user_data['first_name']}. {joke} /n ", reply_markup=main_menu(), parse_mode="Markdown")
    await state.clear()


#@router.message(Reg.speciality)
#async def reg_finish(message: types.Message, state: FSMContext):
    #await state.update_data(speciality=message.text)
    #user_data = await state.get_data()
    # Предполагается, что callback_data уже получено ранее и сохранено в user_data
    #add_user(message.from_user.id, user_data["first_name"], user_data['last_name'], user_data['speciality'])
    #await message.answer(f'Я тебя запомнил, {user_data["first_name"]}')
    #await state.clear()


