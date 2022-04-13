import shelve
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import TMP_DATA, DATABASE
from utils import Database, User


DATA_FROM_MARKUP = ['указать модуль', 'вставить слова самому']
END_MARKUP = ['Давай по новой, Миша...', 'Здесь сессия запрещена. Сессию вырубай...']
STARTING_MARKUP = ['Да!', 'Нет(', 'Выйти']
START_SESSION_MARKUP = ['начать диктант', 'получить слова']
CLOSE_SESSION_MARKUP = ['Разбудить бота']

SB_CLASS_MARKUP = ['7', '8', '9']
SB_MODULE_NUMBER_MARKUP = [str(i) for i in range(1, 7)]
SB_MODULE_ID_MARKUP = ['a', 'b', 'c', 'e', 'f', 'i', 'rus']

is_words_correct = lambda message: all([(line.count(' = ') == 1) for line in message.text.split('\n')])
is_markup_ans_correct = lambda markup: (lambda message: message.text in markup)

database = Database(DATABASE)
users = shelve.open(TMP_DATA, writeback=True)


class Dictation(StatesGroup):
    start_session = State()
    run_dictation = State()
    data_from = State()
    words = State()
    starting_game = State()
    game = State()
    end_game = State()
    close_session = State()


class DictationFromSB(StatesGroup):
    sb_class = State()
    module_number = State()
    module_id = State()


def get_user(message: types.Message) -> User:
    '''
    Узнаем пользователя по его сообщению
    '''
    user_id = str(message.from_user.id)
    user = users.get(user_id)
    return user


def generate_markup(items: list) -> types.ReplyKeyboardMarkup:
    """
    Создаем кастомную клавиатуру для выбора ответа
    """
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for item in list(items):
        markup.add(item)
    return markup


async def define_user(message: types.Message) -> dict:
    return {'user': get_user(message)}



