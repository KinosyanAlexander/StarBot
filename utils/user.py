from random import shuffle
from typing import List
from .dictation_db import DictationDatabase


class User(object):
    def __init__(self, user_id: str):
        self.id = user_id
        self.current = []
        self.sb_data = ['', '', '']
        self.words = []
        self.correct_answers = 0
        self.words_count = 0
        self.counter = 0
        self.wrong_answers = []
    
    def get_words_from_text(self, text: str) -> List[List[str]]:
        '''Берет слова из текста пользователя'''
        data = text.split('\n')
        self.words_count = len(data)
        self.words = list(map(lambda x: x.split(' = '), data))
        shuffle(self.words)
        return self.words
    
    def get_words_from_sb(self, database: DictationDatabase, sb_data: List[str]=[]) -> List[List[str]]:
        '''Берет слова из конкретного модуля из базы данных database'''
        if sb_data:
            self.sb_data = sb_data
        self.words = database.get_module(*self.sb_data)
        self.words_count = len(self.words)
        shuffle(self.words)
        return self.words
    
    def check_answer(self, ans: str) -> bool:
        '''Проверяет ответ на верность'''
        if self.current[0].lower() == ans.lower().strip():
            self.correct_answers += 1
            return True
        else:
            self.wrong_answers.append(self.current)
            return False
    
    def next_word(self) -> List[str]:
        '''Дает следущую пару слов. Если все были выданы, дает ошибку StopIteration'''
        if self.counter == self.words_count:
            raise StopIteration
        self.current = self.words[self.counter]
        self.counter += 1
        return self.current
    
    def get_success(self) -> float:
        '''Возвращает процент правильных ответов'''
        return self.correct_answers / self.words_count * 100
    
    def reset(self) -> None:
        '''Сбрасывает параметры юзера для повторного диктанта'''
        self.current = []
        self.correct_answers = 0
        self.counter = 0
        self.wrong_answers = []
        shuffle(self.words)

    def __repr__(self) -> str:
        return f'<User id: {self.user_id}, is_game: {self.is_game}>'
