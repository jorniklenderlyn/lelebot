from flask import Flask
from data.VKusers import VKuser
from data.db_session import global_init, create_session


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    global_init('db/data.db')


if __name__ == "__main__":
    main()