from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,\
    InlineKeyboardButton, InlineKeyboardMarkup
from schedule import Schedule


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
kco = KeyboardButton("КЦО🏫")
itcube = KeyboardButton("IT-куб")
settings = KeyboardButton("Настройки⚙️")
schedule = KeyboardButton("Расписание 🗓")
teachers = KeyboardButton("Учителя 👨‍🏫")
events = KeyboardButton("События🎉")
eventsnear = KeyboardButton("Ближайшие события")
eventsall = KeyboardButton("Все события")
allteachers = KeyboardButton("Список учителей 📝")
searchteacher = KeyboardButton("Поиск учителя 🔎")
btn = KeyboardButton("btn ")
backbtn = KeyboardButton("<")
changeclass = KeyboardButton("Сменить класс")
andtoto = KeyboardButton("Событ., ФИО учит., и т.д. ...")

MENUkb = ReplyKeyboardMarkup(resize_keyboard=True)
MENUkb = MENUkb.add(kco)
#MENUkb = MENUkb.add(itcube)
MENUkb = MENUkb.add(settings)
KCOkb = ReplyKeyboardMarkup(resize_keyboard=True)
KCOkb = KCOkb.add(schedule).add(events, teachers).add(backbtn)
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
HLPdbkb = HLPdbkb.add(backbtn)
ANDTOTOkb = ReplyKeyboardMarkup(resize_keyboard=True)
ANDTOTOkb = ANDTOTOkb.add(teachers)
ANDTOTOkb = ANDTOTOkb.add(events)
ANDTOTOkb = ANDTOTOkb.add(backbtn)
dictKB = {
    'КЦО🏫': [KCOkb, None, 'S', 1],
    'Настройки⚙️': [HLPdbkb, None, 'S', 1],
    'Событ., ФИО учит., и т.д. ...': [ANDTOTOkb, None, 'S', 1],
    'Учителя 👨‍🏫': [KCOteacherskb, None, 'S', 1],
    'Сменить класс': [inlinekb, 'schedule()', 'H', 0],
    'Расписание 🗓': [inlinekb, 'schedule()', 'H', 1],
    'События🎉': [KCOeventskb, None, 'S', 1],
    'Список учителей 📝': [KCOteacherskb, 'listteachers()', 'S', 1]
}