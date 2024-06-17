from aiogram import types, Router, Dispatcher, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from db import get_user_info, check_user
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import keyboard as kb
from config import bot
from text import text
# Обработчик команды /start
router = Router()
dp = Dispatcher()


#Кому обратная связь
Nazarov = "345418775"
@router.message(Command("start"))
async def cmd_start(message: Message, state = FSMContext):
    user_id = message.from_user.id
    await bot.send_message(chat_id=message.from_user.id, text='...', reply_markup=ReplyKeyboardRemove())
    user_info = get_user_info(user_id)
    if user_info is not None:
        first_name = user_info[1]
        await message.answer(text=f"Привет, {first_name}!", reply_markup=kb.main_old)
    else:
        await message.answer(text=f"Привет! Я тебя пока не знаю. Незнакомцам  свои функции не показываю {message.from_user.id}", reply_markup=kb.main_new)

@router.message(Command("menu"))

async def menu(message: Message, state = FSMContext):
    if check_user(message.from_user.id):
        #await message.answer("Клавиатура удалена", reply_markup=types.ReplyKeyboardRemove())# Пока тут для вычистки стаых клавиатур у юзеров
        #await message.delete_reply_markup(str(message.message_id+1))
        await message.answer(text = text('main'), #'Это главное меню. \n Инфо: там пока ничего нет, но мжет нажать \n Спасибки - Отправка, просмотр спасибок. \n Обратная связь - можешь написать пожелания по работе бота', 
                             reply_markup=kb.main_menu(), parse_mode="Markdown")
    else:
        await message.answer(text=f"Привет! Я тебя пока не знаю. Незнакомцам  свои функции не показываю {message.from_user.id}", reply_markup=kb.main_new)

@router.callback_query(lambda c: c.data=="back_to_main")
async def back_to_menu(callback:types.CallbackQuery):
    await kb.edit_keybaoard(callback,kb.main_menu(), text('main'))


class mess(StatesGroup):
    first = State()
    second = State()

@router.callback_query(lambda c: c.data=="feedback")
async def send_mess(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(mess.first)
    await kb.edit_keybaoard(callback,kb.finish, "Просто отправь анонимное сообщение или вернись в меню")
    #await message.answer(text= "Что хочешь предложить? Это анонимно, поэтому если хочешь чтобы тебе написали, напиши свои данные в конце сообщения")

@router.message(mess.first)
async def send_mess_second(message: Message, state: FSMContext):
    mess_fromusr = message.text
    await state.update_data(first=mess_fromusr)
    for_admin = await state.get_data()
    mess_for_admin = for_admin['first']
    user_id = message.from_user.id
    await bot.send_message(chat_id=Nazarov,text = f'Фидбэк - \n {mess_for_admin}')
    #await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id-1)
    #await message.delete_reply_markup(str(message.message_id-1))
    #await message.answer(text = "Спасибка улетела получателю.", reply_markup= kb.finish_send_ty)
    await bot.send_message(chat_id=user_id,text = "Сообщение отправлено", reply_markup= kb.finish)
    #await kb.edit_keybaoard(callback,kb.finish(), "Просто отправь анонимное сообщение или вернись в меню")
    await state.clear()
@router.callback_query(lambda c: c.data=="info")
async def info(callback: types.CallbackQuery):
    await kb.edit_keybaoard(callback,kb.finish, "Пользуясь отсутствием информации, хочу принести извинения Павлу Москвину за бесконечный спам при первом тесте бота. ")
