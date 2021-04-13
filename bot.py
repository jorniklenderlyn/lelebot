import asyncio
import json
import aioschedule

TOKEN = '1703591338:AAEpyrOMsGzM_0itzM12x6tyxAxJ9a7cC-U'
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import buttons as btns
import database
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


class Schedule:
    def __init__(self, FILENAMEpdf):
        self.FILENAMEpdf = FILENAMEpdf


    def download_pdf(self):
        def check_url(checking_url):
            return checking_url[-1] == "f"


        def get_new_url():
            global html, ind, url_list, flag_url
            new_url = URL
            if ROADFOLDER in html:
                len_html = len(html)
                html = html[html.index(ROADFOLDER):]
                for item in range(len_html):
                    if html[item] != chr(34):
                        new_url += html[item]
                    else:
                        if check_url(new_url):
                            if flag_url:
                                url_list.append(new_url)
                                html = html[item + 1:]
                                get_new_url()
                        else:
                            break


        global html, ind, url_list, flag_url
        flag_url = True
        url_list = list()
        URL = 'http://school.kco27.ru//'
        ROADFOLDER = 'wp-content/uploads/shedule/'
        html = requests.get(URL).text
        ind = html.index(ROADFOLDER)
        html = html[ind:]
        get_new_url()
        print(url_list)
        print(LST_schedule)
        if url_list[-1] in LST_schedule or len(url_list) == 0:
            return None
        else:
            request = requests.get(url_list[-1], stream=True)
            with open(self.FILENAMEpdf, 'wb') as file:
                file.write(request.content)
            LST_schedule.append(url_list[-1])
            return True



    def delete_pdf_imades(self):
        pass


    def get_classes(self):
        text = self.get_text_pdf()
        box = []
        for i in text.split('\n'):
            if '.' in i:
                iq = i.replace('/', '').replace('.', '').replace(' ', '')
                if any([j.isdigit() for j in (iq)]) and iq.isalnum():
                    if len(i.replace(' ', '')) < 8:
                        if len(i.split('.')) == 2 and len(i.split('.')[0]) == 2 and len(i.split('.')[1]) == 2:
                            pass
                        else:
                            if int(i.split('.')[0]) > 9:
                                box.append(i.strip())
                            else:
                                i = i.split()[0]
                                box.append('.'.join(i.replace('.', ' ').strip().split()))
        return box


    def get_class_groupes(self, clas):
        lst = []
        for i in self.get_classes():
            if i.startswith(clas):
                lst.append(i)
        return lst


    def get_phooto_path(self, clas):
        pass


    def get_num_of_borders(self, text):
        numOfborders = 0
        if 'кабинет' in text.lower() or 'каб.' in text.lower():
            numOfborders += 1
        if 'учитель' in text.lower() or 'уч.' in text.lower():
            numOfborders += 1
        return numOfborders


    def get_text_pdf(self):
        txt = ''
        pdf_document = self.FILENAMEpdf
        doc = fitz.open(pdf_document)
        page1 = doc.loadPage(0)
        txt += '\n' + page1.getText("text")
        page1 = doc.loadPage(1)
        txt += '\n' + page1.getText("text")
        page1 = doc.loadPage(2)
        txt += '\n' + page1.getText("text")
        page1 = doc.loadPage(3)
        txt += '\n' + page1.getText("text")
        return txt


    def get_indent(self, pixMap, width, height):
        box = []
        for i in range(height):
            tok = 0
            for j in range(width):
                if pixMap[j, i] == (0, 0, 0):
                    tok += 1
            if tok > 500:
                box.append(i)
        return (box[0], box[-1])


    def make_lessonslists(self, classes, filePath, pdffile):
        global boxOfImages
        try:
            os.makedirs("data")
        except:
            pass

        doc = None
        file = pdffile
        doc = fitz.open(file)
        for i in range(len(doc)):
            first_page = doc[i]

            image_matrix = fitz.Matrix(fitz.Identity)
            image_matrix.preScale(2, 2)

            pix = first_page.getPixmap(alpha=False, matrix=image_matrix)
            boxOfImages.append(f'{i}.jpg')
            pix.writePNG(f'data/{i}.jpg')

        NUMBEROFCLASS = 0
        for _filename_ in boxOfImages:
            img = Image.open(f"{filePath}{_filename_}")
            pixMap = img.load()
            width, height = img.size

            listTemplates = []
            boxTime2 = [False]
            FIRSTindent, SECONDindent = self.get_indent(pixMap, width, height)
            for i in range(FIRSTindent, SECONDindent):
                boxTime = []
                tok = 0
                for j in range(width):
                    if pixMap[j, i] != (0, 0, 0):
                        boxTime.append(True)
                    else:
                        tok += 1
                        boxTime.append(False)
                # print(boxTime)
                if (not all(boxTime2) and all(boxTime)) or (all(boxTime2) and not all(boxTime)):
                    listTemplates.append(i)
                boxTime2 = boxTime.copy()
            listTemplates.extend([FIRSTindent, SECONDindent])
            listTemplates.sort()

            try:
                os.makedirs("data/data")
            except:
                pass

            def getY(y):
                chek = 0
                border = set()
                variableBorder = None
                for i in range(width):
                    if pixMap[i, y] == (0, 0, 0):
                        variableBorder = i
                    elif variableBorder:
                        border.add(variableBorder)
                return sorted(list(border))

            BORDERNUM = self.get_num_of_borders(self.get_text_pdf())
            for i in range(len(listTemplates) // 2):
                try:
                    if 1:
                        y0 = listTemplates[i * 2]
                        y1 = listTemplates[i * 2 + 1]
                        boxBorder = getY(y0 + 3)
                        im0 = img.crop((boxBorder[0], y0, boxBorder[2], y1))
                        for k in range((len(boxBorder) - 3) // BORDERNUM + 1):

                            # print(boxBorder)
                            x0 = boxBorder[k * (BORDERNUM + 1) + 2]
                            x1 = boxBorder[k * (BORDERNUM + 1) + 3 + BORDERNUM]
                            # print(x0, x1)
                            im1 = img.crop((x0, y0, x1 + 1, y1))
                            new_im = Image.new('RGB', (im0.size[0] + im1.size[0], im0.size[1]))
                            new_im.paste(im0, (0, 0))
                            new_im.paste(im1, (im0.size[0], 0))
                            new_im.save('data/data/' + str(classes[NUMBEROFCLASS]) + '.jpg')
                            NUMBEROFCLASS += 1
                except Exception:
                    pass


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
        await callback_query.message.edit_text('/helpKCO')
        await callback_query.answer('Данные успешно сохранены!')
        ph = open('data/data/' + database.get_class_user(callback_query['message']['chat']['id']) + '.jpg', 'rb')
        await bot.send_photo(callback_query['message']['chat']['id'], ph)
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
        Kb = btns.MENUkb
    elif msg.text in btns.dictKB:
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


async def automatic_notification():
    users_lst = database.get_all_class_users()
    print(users_lst)
    for i in users_lst:
        print('i', i)
        for j in list(set(users_lst[i])):
            ph = open('data/data/' + i + '.jpg', 'rb')
            print('j', j)
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

    #thread2 = Thread(target=telebot_main)
    #thread1 = Thread(target=telebot_auto)
    #thread1.start()
    #thread2.start()
    #thread1.join()
    #thread2.join()
    telebot_main()
