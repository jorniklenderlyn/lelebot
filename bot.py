import asyncio
import json
import aioschedule

TOKEN = '1723505895:AAHSHZTPbsD1VcrdK_9usLZJc3Wd824NRIc'
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import buttons as btns
import buttons
import database
from buttons import dynamic_menu_helpDB
import threading
from threading import Thread
import fitz
import os
import time
import requests
import datetime
from PIL import Image

boxOfImages = []
update_hours_list = [6, 15, 16, 18, 23]
url_today = ''
url_to_download = ''
list_with_checklists = []
todaydata = int(datetime.datetime.today().day)
nextdaydata = todaydata + 1
downloading_checklist_now = False
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
LST_schedule = []


from schedule import Schedule


flag_url1 = True
#url_list1 = json.load(open('datajs.json', 'r', encoding='utf-8'))['schedule']
url_list1 = []
MAIN_URL = 'http://school.kco27.ru//'
ROADFOLDER = 'wp-content/uploads/shedule/'
html1 = requests.get(MAIN_URL).text
indexi = html1.index(ROADFOLDER)
html1 = html1[indexi:]


def check_url_from_system():
    global flag_url1, url_list1, MAIN_URL, ROADFOLDER, html1, indexi

    def check_url(checking_url):
        return checking_url[-1] == "f"

    def get_new_url():
        global html1
        new_url = MAIN_URL
        print(url_list1)
        if ROADFOLDER in html1:
            len_html = len(html1)
            html1 = html1[html1.index(ROADFOLDER):]
            for item in range(len_html):
                if html1[item] != chr(34):
                    new_url += html1[item]
                else:
                    if check_url(new_url):
                        if flag_url1:
                            url_list1.append(new_url)
                            html1 = html1[item + 1:]
                            get_new_url()
                    else:
                        break

    def check_urls(url_list_in, todaydata1, nextdaydata1):
        string_from_urls = ''.join(url_list_in)
        if str(nextdaydata1) in string_from_urls:
            return 1
        elif str(todaydata1) in string_from_urls:
            return 2
        else:
            return 0

    get_new_url()
    print(url_list1)
    check_res = check_urls(url_list1, todaydata, nextdaydata)
    return check_res


async def updater_work():
    global downloading_checklist_now
    print(101)
    print("downloading_checklist")
    sch = Schedule('q.pdf')
    if sch.download_pdf():
        sch.make_lessonslists(sch.get_classes(), 'data/', 'q.pdf')
        await automatic_notification()
        print("downloaded_checklist")
        print(f"url_checklist_to_downloud: {url_to_download}")
        downloading_checklist_now = False




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
        #print(database.get_all_class_users())
        await callback_query.message.edit_text('/helpKCO')
        await callback_query.answer('Данные успешно сохранены!')
        #print([database.get_class_user(callback_query['message']['chat']['id'])])
        try:
            ph = open('data/data/' + database.get_class_user(callback_query['message']['chat']['id']) + '.jpg', 'rb')
            await bot.send_photo(callback_query['message']['chat']['id'], ph)
        except:
            print('вы забыли старт')
    elif callback_query.data.startswith('ITcubesection'):
        id_selestion = inline_button_text('ITcubesection', callback_query.data)
        database.change_user_what(callback_query['message']['chat']['id'], id_selestion, 'itcube-section')
        await callback_query.message.edit_text('Расписание ' + database.get_section_name_itcube(id_selestion)[1] + ':')
        await callback_query.answer('Данные успешно сохранены!')
        try:
            for i in database.get_schedule_itcube(id_selestion):
                text = ''
                text += database.get_day(i[2])[1] + '\n'
                text += 'Время начала: ' + str(i[3]) + '\n'
                text += 'Кабинет: ' + str(i[4]) + '\n'
                text += 'Учитель: ' + database.get_teacher(i[5])[1] + '\n'
                await bot.send_message(callback_query['message']['chat']['id'], text)
        except Exception as e:
            print('вы забыли старт')
    await bot.answer_callback_query(callback_query.id)
    #await bot.send_message(callback_query.from_user.id, inline_button_text('classbtn', callback_query.data))


@dp.message_handler(commands=['start'])
async def process_start_command(msg: types.Message):
    database.add_TL_user(msg.from_user.id)
    await msg.reply("Привет!\nДля того чтобы узнать больше напиши /help", reply_markup=btns.MENUkb)


@dp.message_handler(commands=['help'])
async def process_help_command(msg: types.Message):
    database.add_TL_user(msg.from_user.id)
    await msg.reply(open('help.txt', 'r', encoding='utf-8').read(), reply_markup=btns.MENUkb)


@dp.message_handler(commands=['helpKCO'])
async def process_help_command(msg: types.Message):
    database.add_TL_user(msg.from_user.id)
    await msg.reply(open('helpKCO.txt', 'r', encoding='utf-8').read(), reply_markup=btns.KCOkb)


@dp.message_handler(commands=['helpKCO'])
async def process_help_command(msg: types.Message):
    database.add_TL_user(msg.from_user.id)
    await msg.reply(open('helpKCO.txt', 'r', encoding='utf-8').read(), reply_markup=btns.KCOkb)


@dp.message_handler(commands=['helpDB'])
async def process_help_command(msg: types.Message):
    database.add_TL_user(msg.from_user.id)
    await msg.reply(open('helpBD.txt', 'r', encoding='utf-8').read(), reply_markup=buttons.dynamic_menu_helpDB(msg.from_user.id, ''))


@dp.message_handler(commands=['getDB'])
async def process_get_db_file(msg: types.Message):
    database.add_TL_user(msg.from_user.id)
    if msg.from_user.id == 1557734671:
        await bot.send_document(msg.from_user.id, ('KCOdbFORbots.db', open('db/data.db', 'rb')))


@dp.message_handler()
async def echo_message(msg: types.Message):
    print(msg.from_user.id)
    print(msg.text)
    Text = msg.text
    Kb = None
    flag = True
    if msg.text == '↩':
        Text = open('help.txt', 'r', encoding='utf-8').read()
        Kb = btns.MENUkb
    elif msg.text in btns.dictKB:
        boxKB = btns.dictKB[msg.text]
        if boxKB[-2] == 'S':
            Kb = boxKB[0]
            if boxKB[1]:
                Text = eval(boxKB[1])
        elif boxKB[-2] == 'H':
            #проверка на наличие данных
            if msg.text == 'Все события':
                for i in database.get_events('all'):
                    print(90)
                    Eventdict = i
                    flag = False
                    text = ''
                    text += Eventdict['@TITLE']
                    text += '\n' + Eventdict['@DATEOFBUBLICATION']
                    text += '\n' + Eventdict['@DATEOFSTART']
                    text += '\n' + Eventdict['@DATEOFFINISH']
                    text += '\n' + Eventdict['@STATUSOFSPECIALITY']
                    text += '\n' + Eventdict['@STATUSOFSCHOOL']
                    text += '\n' + Eventdict['@STATUSOFCLASS']
                    text += '\n' + Eventdict['@DESCRIPTION']
                    await bot.send_message(msg.from_user.id, text)
            elif msg.text == 'Расписание 🗓':
                if database.chek_user(msg['chat']['id'], 'class') and boxKB[-1]:
                    ph = open('data/data/' + database.get_class_user(msg.from_user.id) + '.jpg', 'rb')
                    await bot.send_photo(msg.from_user.id, ph)
                else:
                    Kb = boxKB[0]
                    Text = 'Укажите свой класс'
            elif msg.text == 'Расписание занятий🗓':
                """
                for i in database.get_schedule_itcube():
                    text = ''
                    for j in i:
                        text += str(j) + '\n'
                    await bot.send_message(msg.from_user.id, text)
                """
                Kb = boxKB[0]
                Text = 'Укажите свою секцию'
            else:
                Kb = boxKB[0]
                Text = 'Укажите свой класс'
        elif boxKB[-2] == 'D':
            boxKB = btns.dictKB[msg.text]
            Kb = eval(boxKB[1].replace('Utl_id', 'msg.from_user.id').replace('msgtext', 'msg.text'))
    if flag:
        await bot.send_message(msg.from_user.id, Text, reply_markup=Kb)


async def automatic_notification():
    users_lst = database.get_all_class_users()
    print(users_lst)
    for i in users_lst:
        if i:
            for j in list(set(users_lst[i])):
                ph = open('data/data/' + i + '.jpg', 'rb')
                await bot.send_photo(j, ph, caption='АВТОМАТ.рассылка^')


def telebot_main():
    global sch
    sch = Schedule('q.pdf')
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)


async def scheduler():
    aioschedule.every().day.at("5:50").do(updater_work)
    aioschedule.every().day.at("6:00").do(updater_work)
    aioschedule.every().day.at("7:00").do(updater_work)
    aioschedule.every().day.at("8:00").do(updater_work)
    aioschedule.every().day.at("9:00").do(updater_work)
    aioschedule.every().day.at("10:00").do(updater_work)
    aioschedule.every().day.at("20:00").do(updater_work)
    aioschedule.every().day.at("21:00").do(updater_work)
    #aioschedule.every().day.at("1:27").do(updater_work)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    telebot_main()
