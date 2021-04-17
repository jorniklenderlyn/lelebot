import sqlalchemy
import sqlite3
from data.db_session import global_init, create_session, create_db, delete_db
from data.VKusers import VKuser
from data.TLusers import TLuser
from data.events import Event


def add_TL_user(Utl_id):
    global_init('kcodbforbots')
    db_sess = create_session()
    if not db_sess.query(TLuser).filter(TLuser.Utl_id == Utl_id).first():
        u = TLuser()
        u.Utl_id = Utl_id
        db_sess.add(u)
        db_sess.commit()


def get_class_user(Utl_id):
    global_init('kcodbforbots')
    db_sess = create_session()
    if db_sess.query(TLuser).filter(TLuser.Utl_id == Utl_id).first():
        return db_sess.query(TLuser).filter(TLuser.Utl_id == Utl_id).first().Uclass
    return None


def change_user_what(Utl_id, hz, param):
    global_init('kcodbforbots')
    db_sess = create_session()
    u = db_sess.query(TLuser).filter(TLuser.Utl_id == Utl_id)
    if param == 'class':
        print('CLASS')
        u.update({TLuser.Uclass: hz}, synchronize_session = False)
    elif param == 'mailing-schedule':
        u.update({TLuser.Umailing_schedule: hz}, synchronize_session=False)
    elif param == 'mailing-events':
        u.update({TLuser.Umailing_events: hz}, synchronize_session=False)
    elif param == 'itcube-section':
        u.update({TLuser.Uitcube_section: hz}, synchronize_session=False)
    db_sess.commit()


def chek_user(Utl_id, param):
    global_init('kcodbforbots')
    db_sess = create_session()
    u = db_sess.query(TLuser).filter(TLuser.Utl_id == Utl_id).first()
    if param == 'class':
        if db_sess.query(TLuser).filter(TLuser.Utl_id == Utl_id).first():
            if u.Uclass:
                return True
    elif param == 'mailing-schedule':
        if u.Umailing_schedule:
            return True
    elif param == 'mailing-events':
        if u.Umailing_events:
            return True
    return False


def get_all_class_users():
    user_dict = dict()
    global_init('kcodbforbots')
    db_sess = create_session()
    for i in db_sess.query(TLuser).all():
        Uid, Uclass = i.Utl_id, i.Uclass
        if Uclass not in user_dict:
            user_dict[Uclass] = [Uid]
        else:
            user_dict[Uclass] = user_dict[Uclass] + [Uid]
    return user_dict


def get_events(param):
    global_init('kcodbforbots')
    db_sess = create_session()
    lst = []
    if param == 'all':
        for i in db_sess.query(Event).all():
            Eventdict = dict()
            Eventdict['@TITLE'] = i.Etitle_of_event
            Eventdict['@DATEOFBUBLICATION'] = str(i.date_of_publiction)
            Eventdict['@DATEOFSTART'] = str(i.Edate_of_start_event)
            Eventdict['@DATEOFFINISH'] = str(i.Edate_of_finish_event)
            Eventdict['@STATUSOFSPECIALITY'] = str(i.Estatus_of_speciality)
            Eventdict['@STATUSOFSCHOOL'] = str(i.Estatus_of_school)
            Eventdict['@STATUSOFCLASS'] = str(i.Estatus_of_class)
            Eventdict['@DESCRIPTION'] = str(i.Edescription)
            lst.append(Eventdict)
    return lst


def get_day(id):
    con = sqlite3.connect("db/db.db")
    cur = con.cursor()
    result = cur.execute("SELECT * FROM days WHERE id = ?;", (id, )).fetchone()
    con.close()
    return result


def get_teacher(id):
    con = sqlite3.connect("db/db.db")
    cur = con.cursor()
    result = cur.execute("SELECT * FROM teachers WHERE id = ?;", (id, )).fetchone()
    con.close()
    return result


def get_schedule_itcube(id):
    con = sqlite3.connect("db/db.db")
    cur = con.cursor()
    if id == 'all':
        result = cur.execute("SELECT * FROM timetable;").fetchall()
    else:
        result = cur.execute("SELECT * FROM timetable WHERE name = ? ORDER BY day ASC;", (id, )).fetchall()
    con.close()
    return result


def get_section_name_itcube(id):
    con = sqlite3.connect("db/db.db")
    cur = con.cursor()
    if id == 'all':
        result = cur.execute("SELECT * FROM names;").fetchall()
    else:
        result = cur.execute("SELECT * FROM names WHERE id = ?;", (id, )).fetchone()
    con.close()
    return result


if __name__ == '__main__':
    #delete_db('kcodbforbots')
    #create_db('kcodbforbots')
    #get_events('all')
    #db_sess = create_session()
    #add_TL_user('888')
    #print(get_all_class_users())
    print(get_schedule_itcube(3))
    pass