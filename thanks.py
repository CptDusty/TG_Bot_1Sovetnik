from aiogram import types, Router, Dispatcher, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile
from db import (get_user_info, check_user, get_users,get_specialities, 
                save_thanks, get_sent_thanks, get_sent_thanks_curr, 
                get_sent_thanks_prev,get_received_thanks_curr,
                get_received_thanks,get_received_thanks_prev,
                get_top_thanks_s, get_top_thanks_curr_s, get_top_thanks_prev_s,
                get_top_thanks_r, get_top_thanks_curr_r, get_top_thanks_prev_r,
                get_specialities, get_users_wspec
                )
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import keyboard as kb
from config import bot
from text import text, button
from collections import defaultdict
router = Router()



#Класс для состояний отправки спасибок
class Send_thank(StatesGroup):
    spec = State()
    reciever = State()
    text = State()

#Обработчик инлайн кнопки спасибки
@router.callback_query(lambda c: c.data == 'thanks')

async def thanks(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    if check_user(callback.from_user.id): #Проверка зареган ли юзер
        await kb.edit_keybaoard(callback,kb.thanks_menu(),text('thanks'))
    else:
        callback.answer(text=f"Привет! Я тебя пока не знаю. Незнакомцам  свои функции не показываю {callback.from_user.id}", reply_markup=kb.main_new)

#Обработчик инлайн кнопки Отправить спасибку
@router.callback_query(lambda c: c.data == 'send_thank')

async def ty_spec(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Send_thank.spec)
    user_id = callback.from_user.id
    await kb.edit_keybaoard(callback,kb.make_spec_ty_keyboard(get_specialities()), text("send_thank"))#(text="Выбери в каком направлении работает получатель", reply_markup=kb.make_spec_ty_keyboard(get_specialities()))
    
#Обработчик коллбека с выбором направления
@router.callback_query(Send_thank.spec) #lambda c: c.data and c.data.startswith('tyspec_'))
async def ty_receiver(callback: types.CallbackQuery, state: FSMContext):
    # Получаем callback_data
    speciality_id = callback.data.replace('tyspec_','')
    #await callback_query.message.delete_reply_markup(str(callback_query.message.message_id))
    if speciality_id != '12':
        await state.update_data(spec=speciality_id)
        await state.set_state(Send_thank.reciever)
        await kb.edit_keybaoard(callback, kb.make_users_keyboard(get_users(callback.from_user.id, speciality_id)), 'Вот список пользователей в этом направлении')
        #await callback.message.answer(text=f'Отлично, вот все пользователи в направлении:', reply_markup = kb.make_users_keyboard(get_users(callback.from_user.id, speciality_id)))
    else:
        await state.set_state(Send_thank.reciever)
        await kb.edit_keybaoard(callback, kb.make_users_keyboard(get_users_wspec(callback.from_user.id)), "Вот список всех пользователей")

@router.callback_query(Send_thank.reciever) #lambda c: c.data and c.data.startswith('reciever_'))
async def ty_text(callback_query: types.CallbackQuery, state: FSMContext):
    #await callback_query.message.delete_reply_markup(str(callback_query.message.message_id))
    #await  callback_query.message.delete_reply_markup(str(callback_query.message.message_id-1))
    reciever_id = callback_query.data.replace('reciever_','')
    await state.update_data(reciever=reciever_id)
    await state.set_state(Send_thank.text)
    await kb.edit_keybaoard(callback_query, kb.auto_ty,f"""Отлично. Теперь введи текст, а также можешь прикрепить любую ссылку.
 \n Кнопка "Просто спасибка" отправит спасибку без текста""")
    print(callback_query.message.message_id)
    #await callback_query.message.answer(text = "Отлично. Теперь введи текст.", reply_markup=kb.auto_ty)

#Отправка и сохранение спасибок
@router.message(Send_thank.text)

async def ty_send(message: Message, state: FSMContext):
    
    tytext = message.text
    await state.update_data(text=tytext)
    
    message_ty = await state.get_data()
    reciever_id = message_ty['reciever']
    text_ty = message_ty['text']
    sender_info = get_user_info(message.from_user.id)
    user_id = message.from_user.id
    save_thanks(message.from_user.id, reciever_id, text_ty)
    #await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    #await message.delete_reply_markup(str(message.message_id-1))
    await bot.send_message(chat_id=user_id,text = "Спасибка улетела получателю.", reply_markup= kb.finish)
    await bot.send_message(chat_id = reciever_id, text= f'Тебе пришла спасибка! \n Текст: {text_ty} \n Отправитель: {sender_info[1]} {sender_info[2]}')
    await state.clear()
@router.callback_query(Send_thank.text)

async def ty_send_auto(callback: types.CallbackQuery, state: FSMContext):
    ty_text = "-"
    await state.update_data(text=ty_text)
    message_ty = await state.get_data()
    reciever_id = message_ty['reciever']
    text_ty = message_ty['text']
    sender_info = get_user_info(callback.from_user.id)
    save_thanks(callback.from_user.id, reciever_id, text_ty)
    await kb.edit_keybaoard(callback, kb.finish, "Спасибка улетела")
    #await callback.answer(text = "Спасибка улетела получателю.", reply_markup= kb.finish_send_ty)
    await bot.send_message(chat_id = reciever_id, text= f'Тебе пришла спасибка!\n Текст: {text_ty}\n Отправитель: {sender_info[1]} {sender_info[2]}\n Вот аудио вместо текста')
    audio = FSInputFile('media/zhil-byl-pes-spasibo-ty-zahodi-esli-chto.mp3')
    await bot.send_voice(chat_id=reciever_id, voice=audio)
    await state.clear()

class My_ty(StatesGroup):
    type = State()
    date = State()
    table = State()
@router.callback_query(lambda c: c.data == 'my_thanks')
async def my_ty(callback:types.CallbackQuery, state: FSMContext):
    await state.set_state(My_ty.type)
    await kb.edit_keybaoard(callback, kb.my_thanks_type(), text('type_thanks'))

@router.callback_query(My_ty.type)
async def my_ty_type(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(type=callback.data)
    await state.set_state(My_ty.date)
    await kb.edit_keybaoard(callback, kb.my_thanks_period(), text('period_thanks'))
    print(callback.data)
@router.callback_query(My_ty.date)
async def my_ty_date(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(date=callback.data)
    await state.set_state(My_ty.table)

    table_data = await state.get_data()
    table_type = table_data['type']
    table_period = table_data['date']
    id = callback.from_user.id

    
    if table_type == "sent_thanks":
        if table_period == "all_period":
            table = get_sent_thanks(id)
        elif table_period == "curr_period":
            table = get_sent_thanks_curr(id)
        elif table_period == "prev_period":
            table = get_sent_thanks_prev(id)
        text = "Отправлено спасибок"
    elif table_type== "rec_thanks":
        if table_period == "all_period":
            table = get_received_thanks(id)
        elif table_period == "curr_period":
            table = get_received_thanks_curr(id)
        elif table_period == "prev_period":
            table = get_received_thanks_prev(id)
        text = "Получено спасибок"
    else:
        table = []

    if len(table)>0:
        user_messages = defaultdict(list)
        for row in table:
            user_messages[(row[0], row[1])].append(row[2])

        table_text = "<pre>\n"  # Используем тег <pre> для сохранения форматирования
        for user, messages in user_messages.items():
            table_text += f"Пользователь: {user[0]}  {user[1]}\nТексты:\n"
            for message in messages:
                table_text += f"- {message}\n"
            table_text += "\n"
        table_text += "</pre>"
        table_text +=f"{text}: {len(table)}"
        await kb.edit_keybaoard_html(callback, kb.finish_my_thanks,table_text)
        #await callback.message.answer(text= f'{text} {len(table)}', reply_markup=ReplyKeyboardRemove())
        #await callback.message.answer(text=table_text,reply_markup= kb.finish_my_thanks ,parse_mode='HTML')
    else: 
        await kb.edit_keybaoard_html(callback, kb.finish_my_thanks,"Тут два варианта - или пока тут пусто, или бот поломался. Но в любом случае не переживай, ты молодец🤩")
        #await callback.message.answer(text= "Тут два варианта - или пока тут пусто, или бот поломался. Но в любом случае не переживай, ты молодец🤩", reply_markup=ReplyKeyboardRemove())

class Top(StatesGroup):
    type_top = State()
    period_top = State()
    table = State()

@router.callback_query(lambda c: c.data == 'top_thanks')
async def my_ty(callback:types.CallbackQuery, state: FSMContext):
    await state.set_state(Top.type_top)
    await kb.edit_keybaoard(callback, kb.my_thanks_type(), text('type_thanks'))

@router.callback_query(Top.type_top)
async def get_top(callback: types.CallbackQuery, state: FSMContext):
    ty_type = callback.data
    await state.update_data(type_top=ty_type)
    await state.set_state(Top.period_top)
    await kb.edit_keybaoard(callback,kb.top_period(), "За какой период сформировать ТОП?")
    #await message.answer(text='За какой период хочешь посмотреть?', reply_markup=kb.my_ty_period)

@router.callback_query(Top.period_top)
async def top_table(callback: types.CallbackQuery, state: FSMContext):
    ty_period = callback.data
    await state.update_data(period_top=ty_period)
    await state.set_state(Top.table)
    data = await state.get_data()
    period = data['period_top']
    type_top = data["type_top"]
    id = callback.from_user.id
    if type_top == "rec_thanks":
        if period == "all_period":
            table = get_top_thanks_r()
        elif period == "curr_period":
            table = get_top_thanks_curr_r()
        elif period == "prev_period":
            table = get_top_thanks_prev_r()
        #table +=f"ТОП полученных"
    elif type_top == "sent_thanks":
        if period == "all_period":
            table = get_top_thanks_s()
        elif period == "curr_period":
            table = get_top_thanks_curr_s()
        elif period == "prev_period":
            table = get_top_thanks_prev_s()
        #table +=f"ТОП отправленных"
    if len(table)>0:
        table_text = "<pre>\n"  # Используем тег <pre> для сохранения форматирования
        for row in table:
            table_text += f"Пользователь: {row[0]}  {row[1]}\nКол-во: {row[2]}\n\n"
        table_text += "</pre>"
        await kb.edit_keybaoard_html(callback, kb.finish_top_thanks,table_text)
        await state.clear()
    else: 
        await kb.edit_keybaoard_html(callback, kb.finish_top_thanks,"Таблица пустая, но в моем алгоритме ты ТОП-1")

        await state.set_state(Top.period_top)
        
    