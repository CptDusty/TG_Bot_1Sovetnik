from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from db import get_users, get_specialities
from aiogram import types
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import bot
from text import button

async def edit_keybaoard(callback: types.CallbackQuery, keyboard, text:str):
    await bot.edit_message_text(text = text, chat_id=callback.message.chat.id,
                                    message_id= callback.message.message_id, reply_markup=keyboard, parse_mode='Markdown')
async def edit_keybaoard_html(callback: types.CallbackQuery, keyboard, text:str):
    await bot.edit_message_text(text = text, chat_id=callback.message.chat.id,
                                    message_id= callback.message.message_id, reply_markup=keyboard, parse_mode='HTML')
def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True, one_time_keyboard=True)
#Уровень 1 - Меню
def main_menu() -> InlineKeyboardButton:
    info = [InlineKeyboardButton(text="Информация", callback_data='info')]
    thanks = [InlineKeyboardButton(text="Спасибки", callback_data='thanks')]
    feedback = [InlineKeyboardButton(text="Отправить обратную связь", callback_data='feedback')]
    return InlineKeyboardMarkup(inline_keyboard=[info,thanks,feedback])

def make_spec_keyboard_for_reg(items: list[str]) -> InlineKeyboardMarkup:
    row = [[InlineKeyboardButton(text=f'{item[1]}', callback_data=f'spec_{item[0]}')] for item in items]
    row.append([InlineKeyboardButton(text=button('back'), callback_data= 'registration')])
    return InlineKeyboardMarkup(inline_keyboard=row)
#Уровень 2 - Спасибки
def thanks_menu() -> InlineKeyboardButton:
    send_ty = [InlineKeyboardButton(text=button('send_ty'), callback_data='send_thank')]
    my_thanks = [InlineKeyboardButton(text=button('my_ty'), callback_data='my_thanks')]
    top_thanks = [InlineKeyboardButton(text=button('top_ty'), callback_data='top_thanks')]
    back = [InlineKeyboardButton(text=button('back'), callback_data='back_to_main')]
    return InlineKeyboardMarkup(inline_keyboard=[send_ty,my_thanks,top_thanks,back])

def my_thanks_type() -> InlineKeyboardButton:
    sent_ty = [InlineKeyboardButton(text=button('sent_ty'), callback_data='sent_thanks')]
    rec_ty = [InlineKeyboardButton(text=button('rec_ty'), callback_data='rec_thanks')]
    back = [InlineKeyboardButton(text=button('back'), callback_data='thanks')]
    return InlineKeyboardMarkup(inline_keyboard=[sent_ty,rec_ty,back])

def my_thanks_period() -> InlineKeyboardButton:
    prev = [InlineKeyboardButton(text=button('prev_period'), callback_data='prev_period')]
    curr = [InlineKeyboardButton(text=button('curr_period'), callback_data='curr_period')]
    all_ty = [InlineKeyboardButton(text=button('all_period'), callback_data='all_period')]
    back = [InlineKeyboardButton(text=button('back'), callback_data='my_thanks')]
    return InlineKeyboardMarkup(inline_keyboard=[prev,curr,all_ty,back])

def top_period() -> InlineKeyboardButton:
    prev = [InlineKeyboardButton(text=button('prev_period'), callback_data='prev_period')]
    curr = [InlineKeyboardButton(text=button('curr_period'), callback_data='curr_period')]
    all_ty = [InlineKeyboardButton(text=button('all_period'), callback_data='all_period')]
    back = [InlineKeyboardButton(text=button('back'), callback_data='thanks')]
    return InlineKeyboardMarkup(inline_keyboard=[prev,curr,all_ty,back])

def make_spec_keyboard(items: list[str]) -> InlineKeyboardMarkup:
    row = [[InlineKeyboardButton(text=f'{item[1]}', callback_data=f'spec_{item[0]}')] for item in items]
    row.append([InlineKeyboardButton(text=button('back'), callback_data= 'send_thank')])
    return InlineKeyboardMarkup(inline_keyboard=row)

def make_spec_ty_keyboard(items: list[str]) -> InlineKeyboardMarkup:
    row = [[InlineKeyboardButton(text=f'{item[1]}', callback_data=f'tyspec_{item[0]}')] for item in items]
    #row.append([InlineKeyboardButton(text=button('idk_ty'), callback_data= 'idk_spec_ty')])
    row.append([InlineKeyboardButton(text=button('back'), callback_data= 'thanks')])
    return InlineKeyboardMarkup(inline_keyboard=row)

#Если пользователь сильно ленивый
auto_ty = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text = 'Просто спасибка', callback_data = "simple_ty")],
    [InlineKeyboardButton(text = 'Назад', callback_data = "send_thank")]
])
finish = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text = 'Вернутся в главное меню', callback_data = "back_to_main")],
])

finish_my_thanks = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text = 'Назад', callback_data = "my_thanks")],
    [InlineKeyboardButton(text = 'Главное меню', callback_data = "back_to_main")]
])
finish_top_thanks = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text = 'Назад', callback_data = "top_thanks")],
    [InlineKeyboardButton(text = 'Главное меню', callback_data = "back_to_main")]
])

button_main_menu = ["Инфо",
                    "Спасибки",
                    "Отправить предложение"]
button_thanks = ["Отправить спасибку",
                 "Мои спасибки",
                 "ТОП"]
button_myty = ["Отправленные",
                 "Полученные",]
button_period = ["За текущий месяц",
                 "За прошлый месяц",
                 "За все время"]
menu_main = make_row_keyboard(button_main_menu)
thanks = make_row_keyboard(button_thanks)
my_ty = make_row_keyboard(button_myty)
my_ty_period = make_row_keyboard(button_period)

main_new = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text = 'Регистрация', callback_data = "registration")]
])

main_old = InlineKeyboardMarkup(inline_keyboard= [
    [InlineKeyboardButton(text = 'Изменить данные', callback_data = "registration")],[InlineKeyboardButton(text=button('main'), callback_data='back_to_main')]
])


def users_list(user_id):
    users = get_users(user_id)
    users_list = make_row_keyboard(users)
    return users_list

#def make_users_keyboard() -> ReplyKeyboardMarkup:
    """
    Создает клавиатуру с кнопками для каждого пользователя.
    Каждая кнопка содержит имя и фамилию пользователя, а user_id используется для отправки сообщений.
    """
    users = get_users()
    # Создаем список списков кнопок
    keyboard_buttons = [[KeyboardButton(text=f"{user[1]} {user[2]}")] for user in users]
    # Создаем клавиатуру
    keyboard = ReplyKeyboardMarkup(keyboard=keyboard_buttons, resize_keyboard=True, one_time_keyboard=True)
    return keyboard

def make_users_keyboard(items: list[str]) -> InlineKeyboardMarkup:
    row = [[InlineKeyboardButton(text=f'{item[1]} {item[2]}', callback_data=f'reciever_{item[0]}')] for item in items]
    row.append([InlineKeyboardButton(text=button('back'), callback_data= 'send_thank')])
    return InlineKeyboardMarkup(inline_keyboard=row)
