from data.db_session import global_init, create_session
from data.VKusers import VKuser
from data.TLusers import TLuser


def add_TL_user(Utl_id):
    global_init('db/data.db')
    db_sess = create_session()
    u = TLuser()
    u.Utl_id = Utl_id
    db_sess.add(u)
    db_sess.commit()


def get_class_user(Utl_id):
    global_init('db/data.db')
    db_sess = create_session()
    if db_sess.query(TLuser).filter(TLuser.Utl_id == Utl_id).first():
        return db_sess.query(TLuser).filter(TLuser.Utl_id == Utl_id).first().Uclass
    return None


def change_user_what(Utl_id, hz, k):
    global_init('db/data.db')
    db_sess = create_session()
    if k == 'class':
        u = db_sess.query(TLuser).filter(TLuser.Utl_id == Utl_id)
        u.update({TLuser.Uclass: hz}, synchronize_session = False)
    db_sess.commit()



def chek_user(Utl_id, k):
    global_init('db/data.db')
    db_sess = create_session()
    if k == 'class':
        if db_sess.query(TLuser).filter(TLuser.Utl_id == Utl_id).first():
            u = db_sess.query(TLuser).filter(TLuser.Utl_id == Utl_id).first()
            if u.Uclass:
                return True
    return False


if __name__ == '__main__':
    change_user_what('1557734671', None, 'class')
    print(chek_user('1557734671', 'class'))