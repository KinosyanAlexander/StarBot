from random import shuffle


class User(object):
    def __init__(self, user_id):
        self.id = user_id
        self.current = []
        self.data_from = 'self'
        self.sb_data = ['', '', '']
        self.words = []
        self.correct_answers = 0
        self.words_count = 0
        self.counter = 0
        self.wrong_answers = []
    
    def get_words_from_text(self, text):
        data = text.split('\n')
        self.words_count = len(data)
        self.words = list(map(lambda x: x.split(' = '), data))
        shuffle(self.words)
        return self.words
    
    def get_words_from_sb(self, database, sb_data=[]):
        if sb_data:
            self.sb_data = sb_data
        self.words = database.get_module(*self.sb_data)
        self.words_count = len(self.words)
        shuffle(self.words)
        return self.words
    
    def check_answer(self, ans):
        if self.current[0] == ans.strip():
            self.correct_answers += 1
            return True
        else:
            self.wrong_answers.append(self.current)
            return False
    
    def next_word(self):
        if self.counter == self.words_count:
            raise StopIteration
        self.current = self.words[self.counter]
        self.counter += 1
        return self.current
    
    def get_success(self):
        return self.correct_answers / self.words_count * 100
    
    def reset(self):
        self.current = []
        self.correct_answers = 0
        self.counter = 0
        self.wrong_answers = []
        shuffle(self.words)

    def __repr__(self):
        return f'<User id: {self.user_id}, is_game: {self.is_game}>'
