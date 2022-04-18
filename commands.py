import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from bot import dp

from utils import User, users, database
from utils import Dictation, DictationFromSB
from utils import DATA_FROM_MARKUP, END_MARKUP, STARTING_MARKUP
from utils import SB_CLASS_MARKUP, SB_MODULE_NUMBER_MARKUP, SB_MODULE_ID_MARKUPS
from utils import START_SESSION_MARKUP, CLOSE_SESSION_MARKUP
from utils import is_markup_ans_correct, is_words_correct, is_module_id_ans_correct
from utils import generate_markup, define_user


@dp.message_handler(commands=["start"], state='*')
@dp.message_handler(is_markup_ans_correct(CLOSE_SESSION_MARKUP), state=Dictation.close_session)
async def start(message: types.Message):
    '''
    Приветствие. Начально меню. Начало сессии. В users добавляет пользователя (класс User).
    '''
    user_id = str(message.from_user.id)
    users[user_id] = User(user_id)
    logging.info(f'Creating session for user {user_id}')

    ans = 'Приветствую.\n\nЯ бот, призванный помочь ученикам средней школы в изучении английского языка.\n'
    ans += 'Я помогу быстро заучивать слова на диктант, используя технологию мини-диктантов.\n\n'
    ans += 'Пройдя несколько раз диктант, вы уже запомните все слова, '
    ans += 'потратив на это значительно меньше времени, чем просто сидя и заучивая их.\n\n'
    ans += 'Для начала диктанта нажмите кнопку "начать диктант"\n'
    ans += 'Если хотите просто получить слова для заучивания из учебника, нажмите "получить слова"'
    ans += '\n\nЕсли возникнут какие-то проблемы, всегда можете вызвать команду /exit'
    
    await message.answer(ans, reply_markup=generate_markup(START_SESSION_MARKUP))
    await Dictation.start_session.set()


@dp.message_handler(define_user, state='*', commands='exit')
async def exit_session(message: types.Message, user: User, state: FSMContext):
    '''Закрытие сессии. После этого остается кнопка, чтобы включить бота.'''
    await state.finish()
    # try:
    #     del users[str(message.from_user.id)]
    # except KeyError:
    #     pass
    logging.info(f'Canceled session for user {str(message.from_user.id)}')
    await message.answer('Ну лады. До скорого.', reply_markup=generate_markup(CLOSE_SESSION_MARKUP))
    await Dictation.close_session.set()


@dp.message_handler(define_user, is_markup_ans_correct(START_SESSION_MARKUP), state=Dictation.start_session)
async def choose_option(message: types.Message, user: User, state: FSMContext):
    '''
    В зависимости от выбранной опции реализует разные сценарии (диктант/выдача слов)
    '''
    if message.text == START_SESSION_MARKUP[0]:
        await run_dictation(message, user)
    else:
        await exit_session(message, user, state)


@dp.message_handler(define_user, commands=["run"])
async def run_dictation(message: types.Message, user: User):
    '''
    Начинает формировать диктант, спрашивает, каким способом он задается.
    '''
    await message.answer('Как зададите диктант?', reply_markup=generate_markup(DATA_FROM_MARKUP))
    await Dictation.data_from.set()


@dp.message_handler(define_user, is_markup_ans_correct(DATA_FROM_MARKUP), state=Dictation.data_from)
async def set_data_from(message: types.Message, user: User):
    '''В зависимости от выбора загрузки слов реализует разные сценарии (самовывоз/из учебника)'''
    if message.text == DATA_FROM_MARKUP[1]: # self
        await message.answer('Введите слова в формате:\n\neng1 = rus2\neng2 = rus2\n...')
        await Dictation.words.set()
    elif message.text == DATA_FROM_MARKUP[0]: # module
        await DictationFromSB.sb_class.set()
        await message.answer('Выберите класс:', reply_markup=generate_markup(SB_CLASS_MARKUP))


@dp.message_handler(define_user, is_markup_ans_correct(SB_CLASS_MARKUP), state=DictationFromSB.sb_class)
async def get_sb_class(message: types.Message, user: User):
    '''Фиксирует информацию о классе. Далее спрашивает про модуль.'''
    user.sb_data[0] = message.text
    await DictationFromSB.module_number.set()
    await message.answer('Какой модуль интересует?', reply_markup=generate_markup(SB_MODULE_NUMBER_MARKUP))


@dp.message_handler(define_user, is_markup_ans_correct(SB_MODULE_NUMBER_MARKUP), state=DictationFromSB.module_number)
async def get_module_number(message: types.Message, user: User):
    '''Фиксирует информацию о модуле. Далее спрашивает про подмодуль.'''
    user.sb_data[1] = message.text
    await DictationFromSB.module_id.set()
    await message.answer('Какой подраздел модуля интересует?', reply_markup=generate_markup(SB_MODULE_ID_MARKUPS[user.sb_data[0]]))


@dp.message_handler(define_user, is_module_id_ans_correct, state=DictationFromSB.module_id)
async def get_module_id(message: types.Message, user: User):
    '''Формирует диктант (из учебника). Спрашивает о готовности начать.'''
    user.sb_data[2] = message.text
    user.get_words_from_sb(database)
    
    await message.answer('Готовы начать мини-диктант?', reply_markup=generate_markup(STARTING_MARKUP))
    await Dictation.starting_game.set()


@dp.message_handler(define_user, is_words_correct, state=Dictation.words)
async def set_self_words(message: types.Message, user: User):
    '''Формирует диктант (из самовывоза). Спрашивает о готовности начать.'''
    user.get_words_from_text(message.text)

    await message.answer('Готовы начать мини-диктант?', reply_markup=generate_markup(STARTING_MARKUP))
    await Dictation.starting_game.set()


@dp.message_handler(define_user, is_markup_ans_correct(STARTING_MARKUP), state=Dictation.starting_game)
async def starting(message: types.Message, user: User, state: FSMContext):
    '''Начинает диктант, жели этого хочет пользователь'''
    if message.text == STARTING_MARKUP[0]: # Yes
        await Dictation.game.set()
        await message.answer('Хорошо. Тогда начнем.')
        await game(message, user, first=True)
    elif message.text == STARTING_MARKUP[1]: # No
        await message.answer('Хорошо, мы подождем...\nТак ты готов?', reply_markup=generate_markup(STARTING_MARKUP))
    elif message.text == STARTING_MARKUP[2]: # Exit
        # await message.answer('Ладно, приходите еще!')
        await exit_session(message, user, state)


@dp.message_handler(define_user, state=Dictation.game)
async def game(message: types.Message, user: User, first=False):
    '''Реализация мини-диктанта'''
    if not first:
        success = user.check_answer(message.text)
        if success:
            await message.answer('Харош! Все верно!')
        else:
            await message.answer(f'Неа! Правильно будет:\n\n{user.current[0]}')
    try:
        word = str(user.next_word()[1])
        await message.answer(f'Переведи:\n\n{word}')
        # await message.answer(word)
    except StopIteration:
        await message.answer('Поздравляю! вы ответили правильно на {:.2f}% вопросов.'.format(user.get_success()))
        if user.get_success() < 100:
            wrong_answers_text = '\n'.join(list(map(lambda x: ' = '.join(x), user.wrong_answers)))
            await message.answer(f'Вот слова, которые тебе стоит подучить:\n\n{wrong_answers_text}')
        await message.answer('Хотите ли повторить или окончить сессию?', reply_markup=generate_markup(END_MARKUP))
        await Dictation.end_game.set()


@dp.message_handler(define_user, is_markup_ans_correct(END_MARKUP), state=Dictation.end_game)
async def end_game(message: types.Message, user: User, state: FSMContext):
    '''В зависимости от желания пользователя возобнавляет игру или закрывает сессию'''
    if message.text == END_MARKUP[0]: # restart
        await Dictation.game.set()
        user.reset()
        await message.answer('Ок. Пошли заново:')
        await game(message, user, first=True)
    elif message.text == END_MARKUP[1]: # end
        # await message.answer('Ну лады. До скорого.')
        await exit_session(message, user, state)


@dp.message_handler(define_user, state='*')
async def incorrect_msg_process(message: types.Message, user: User):
    '''Обработка некорректного ввода данных'''
    await message.answer('Ты, наверное, что-то попутал. Введи корректные данные пожожуста')
