from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,\
    InlineKeyboardButton, InlineKeyboardMarkup
from schedule import Schedule
from data.db_session import global_init, create_session
import database


#--inline--
sch = Schedule('q.pdf')
inlinekb = InlineKeyboardMarkup()
lst = []
for i in sch.get_classes():
    clas = i.split('.')[0]
    if clas not in lst:
        inlinebtn = InlineKeyboardButton(clas, callback_data='classbtn' + clas)
        inlinekb = inlinekb.insert(inlinebtn)
        lst.append(clas)
#--inline
#--inline--
ITcubeinlinekb = InlineKeyboardMarkup()
for i in database.get_section_name_itcube('all'):
    ITcubeinlinebtn = InlineKeyboardButton(i[1], callback_data='ITcubesection' + str(i[0]))
    ITcubeinlinekb = ITcubeinlinekb.insert(ITcubeinlinebtn)
#--inline
kco = KeyboardButton("КЦО🏫")
itcube = KeyboardButton("IT-куб")
settings = KeyboardButton("Настройки⚙️")
schedule = KeyboardButton("Расписание 🗓")
scheduleitcube = KeyboardButton("Расписание занятий🗓")
teachers = KeyboardButton("Учителя 👨‍🏫")
events = KeyboardButton("События🎉")
eventsnear = KeyboardButton("Ближайшие события")
eventsall = KeyboardButton("Все события")
allteachers = KeyboardButton("Список учителей 📝")
searchteacher = KeyboardButton("Поиск учителя 🔎")
btn = KeyboardButton("btn ")
backbtn = KeyboardButton("↩")
changeclass = KeyboardButton("Сменить класс🆙")
andtoto = KeyboardButton("Событ., ФИО учит., и т.д. ...")
changemailingScheduleNO = KeyboardButton("Рассылка расписания🟥")
changemailingScheduleYES = KeyboardButton("Рассылка расписания🟩")
changemailingEventsNO = KeyboardButton("Рассылка Событий      🟥")
changemailingEventsYES = KeyboardButton("Рассылка Событий      🟩")

MENUkb = ReplyKeyboardMarkup(resize_keyboard=True)
MENUkb = MENUkb.add(kco)
MENUkb = MENUkb.add(itcube)
#MENUkb = MENUkb.add(itcube)
MENUkb = MENUkb.add(settings)

KCOkb = ReplyKeyboardMarkup(resize_keyboard=True)
KCOkb = KCOkb.add(events, schedule, teachers).add(changeclass).add(backbtn)

ITcubekb = ReplyKeyboardMarkup(resize_keyboard=True)
ITcubekb = ITcubekb.add(scheduleitcube)
ITcubekb = ITcubekb.add(backbtn)

KCOteacherskb = ReplyKeyboardMarkup(resize_keyboard=True)
KCOteacherskb = KCOteacherskb.add(allteachers)
KCOteacherskb = KCOteacherskb.add(searchteacher)
KCOteacherskb = KCOteacherskb.add(backbtn)
KCOeventskb = ReplyKeyboardMarkup(resize_keyboard=True)
KCOeventskb = KCOeventskb.add(eventsall)
KCOeventskb = KCOeventskb.add(eventsnear)
KCOeventskb = KCOeventskb.add(backbtn)

HLPdbkb = ReplyKeyboardMarkup(resize_keyboard=True)
HLPdbkb = HLPdbkb.add(changeclass)
HLPdbkb = HLPdbkb.add(changemailingScheduleYES)
HLPdbkb = HLPdbkb.add(backbtn)

ANDTOTOkb = ReplyKeyboardMarkup(resize_keyboard=True)
ANDTOTOkb = ANDTOTOkb.add(teachers)
ANDTOTOkb = ANDTOTOkb.add(events)
ANDTOTOkb = ANDTOTOkb.add(backbtn)
"""
S - simple простая кнопка, после нажатия которой меняется меню.
H - hard кнопка вызывает функцию или что то делает.
D - dynamic кнопка меняет свой облик
Все эти приставки указ. в словаре для сокращения кода.
"""
dictKB = {
    'КЦО🏫': [KCOkb, None, 'S', 1],
    'IT-куб': [ITcubekb, None, 'S', 1],
    'Настройки⚙️': [None, 'buttons.dynamic_menu_helpDB(Utl_id, msgtext)', 'D', 1],
    'Событ., ФИО учит., и т.д. ...': [ANDTOTOkb, None, 'S', 1],
    'Учителя 👨‍🏫': [KCOteacherskb, None, 'S', 1],
    'Сменить класс🆙': [inlinekb, 'schedule()', 'H', 0],
    'Расписание 🗓': [inlinekb, 'schedule()', 'H', 1],
    'Расписание занятий🗓': [ITcubeinlinekb, 'schedule()', 'H', 1],
    'Все события': [None, None, 'H', 1],
    'События🎉': [KCOeventskb, None, 'S', 1],
    'Рассылка расписания🟥': [None, 'buttons.dynamic_menu_helpDB(Utl_id, msgtext)', 'D', 1],
    'Рассылка расписания🟩': [None, 'buttons.dynamic_menu_helpDB(Utl_id, msgtext)', 'D', 1],
    'Рассылка Событий      🟥': [None, 'buttons.dynamic_menu_helpDB(Utl_id, msgtext)', 'D', 1],
    'Рассылка Событий      🟩': [None, 'buttons.dynamic_menu_helpDB(Utl_id, msgtext)', 'D', 1],
    'Список учителей 📝': [KCOteacherskb, 'listteachers()', 'S', 1]
}

def dynamic_menu_helpDB(Utl_id, msgtext):
    if msgtext == 'Рассылка расписания🟥':
        database.change_user_what(Utl_id, True, 'mailing-schedule')
    elif msgtext == 'Рассылка расписания🟩':
        database.change_user_what(Utl_id, False, 'mailing-schedule')
    elif msgtext == 'Рассылка Событий      🟥':
        database.change_user_what(Utl_id, True, 'mailing-events')
    elif msgtext == 'Рассылка Событий      🟩':
        database.change_user_what(Utl_id, False, 'mailing-events')
    HLPdbkb = ReplyKeyboardMarkup(resize_keyboard=True)
    #HLPdbkb = HLPdbkb.add(changeclass)
    if database.chek_user(Utl_id, 'mailing-schedule'):
        HLPdbkb = HLPdbkb.add(changemailingScheduleYES)
    if not database.chek_user(Utl_id, 'mailing-schedule'):
        HLPdbkb = HLPdbkb.add(changemailingScheduleNO)
    if database.chek_user(Utl_id, 'mailing-events'):
        HLPdbkb = HLPdbkb.add(changemailingEventsYES)
    if not database.chek_user(Utl_id, 'mailing-events'):
        HLPdbkb = HLPdbkb.add(changemailingEventsNO)
    HLPdbkb = HLPdbkb.add(backbtn)
    return HLPdbkb