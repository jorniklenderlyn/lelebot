TOKEN = '1703591338:AAEpyrOMsGzM_0itzM12x6tyxAxJ9a7cC-U'
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import buttons as btns
from schedule import Schedule
import database

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


def listteachers():
    return 'Список учителей'


def schedule():
    return 'Расписание'


def inline_button_text(name, data):
    print(data.replace(name, ''))
    return data.replace(name, '')


@dp.callback_query_handler()
async def process_callback_button1(callback_query: types.CallbackQuery):
    if callback_query.data.startswith('classbtn'):
        inlinekb2 = InlineKeyboardMarkup()
        for i in sch.get_class_groupes(inline_button_text('classbtn', callback_query.data)):
            inlinebtn2 = InlineKeyboardButton(i, callback_data='groupbtn' + i)
            inlinekb2 = inlinekb2.insert(inlinebtn2)
        #print(sch.get_class_groupes(inline_button_text('classbtn', callback_query.data)))
        await callback_query.message.edit_text('Выберите группу', reply_markup=inlinekb2)
    elif callback_query.data.startswith('groupbtn'):
        database.change_user_what(callback_query['message']['chat']['id'],
                                  inline_button_text('groupbtn', callback_query.data), 'class')
        await callback_query.message.edit_text('/helpKCO')
        await callback_query.answer('Данные успешно сохранены!')
        ph = open('data/data/' + database.get_class_user(callback_query['message']['chat']['id']) + '.jpg', 'rb')
        await bot.send_photo(callback_query['message']['chat']['id'], ph)
    await bot.answer_callback_query(callback_query.id)
    #await bot.send_message(callback_query.from_user.id, inline_button_text('classbtn', callback_query.data))


@dp.message_handler(commands=['start'])
async def process_start_command(msg: types.Message):
    database.add_TL_user(msg.from_user.id)
    await msg.reply("Привет!\nДля того чтобы узнать больше напиши /help", reply_markup=btns.KCOkb)


@dp.message_handler(commands=['help'])
async def process_help_command(msg: types.Message):
    database.add_TL_user(msg.from_user.id)
    await msg.reply(open('help.txt', 'r', encoding='utf-8').read(), reply_markup=btns.KCOkb)


@dp.message_handler(commands=['helpKCO'])
async def process_help_command(msg: types.Message):
    database.add_TL_user(msg.from_user.id)
    await msg.reply(open('helpKCO.txt', 'r', encoding='utf-8').read(), reply_markup=btns.KCOkb)


@dp.message_handler(commands=['helpKCO'])
async def process_help_command(msg: types.Message):
    database.add_TL_user(msg.from_user.id)
    await msg.reply(open('helpKCO.txt', 'r', encoding='utf-8').read(), reply_markup=btns.KCOkb)


@dp.message_handler(commands=['helpBD'])
async def process_help_command(msg: types.Message):
    database.add_TL_user(msg.from_user.id)
    await msg.reply(open('helpBD.txt', 'r', encoding='utf-8').read(), reply_markup=btns.HLPdbkb)


@dp.message_handler()
async def echo_message(msg: types.Message):
    print(msg.from_user.id)
    Text = msg.text
    Kb = None
    if msg.text == '<':
        Text = open('help.txt', 'r', encoding='utf-8').read()
        Kb = types.ReplyKeyboardRemove()
    if msg.text in btns.dictKB:
        boxKB = btns.dictKB[msg.text]
        if boxKB[-2] == 'S':
            Kb = boxKB[0]
            if boxKB[1]:
                Text = eval(boxKB[1])
        elif boxKB[-2] == 'H':
            #проверка на наличие данных
            if database.chek_user(msg['chat']['id'], 'class') and boxKB[-1]:
                ph = open('data/data/' + database.get_class_user(msg.from_user.id) + '.jpg', 'rb')
                await bot.send_photo(msg.from_user.id, ph)
            else:
                Kb = boxKB[0]
                Text = 'Укажите свой класс'

    await bot.send_message(msg.from_user.id, Text, reply_markup=Kb)


if __name__ == '__main__':
    sch = Schedule('q.pdf')
    executor.start_polling(dp)