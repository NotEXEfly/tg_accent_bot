import re
from bs4 import BeautifulSoup
import requests
from time import sleep


class Accent():
    def __init__(self, user_input):
        self.clear_input = list(
            set(re.findall(r'[A-яё]+', user_input.lower())))
        self.__status_word = True
        self.answer_arr = self.__create_accent_arr(self.clear_input)
        self.is_solo_word = len(self.answer_arr) == 1 or len(
            self.answer_arr) == 0

    ACCENTS = {'А': 'а́', 'Е': 'е́',
               'И': 'и́', 'О': 'о́',
               'У': 'у́', 'Ы': 'ы́',
               'Э': 'э́', 'Ю': 'ю́',
               'Я': 'я́', }

    def __create_accent_arr(self, clear_data):
        counter = 0
        data = []
        for word in clear_data:
            if len(word) < 4:
                continue
            if counter == len(clear_data) // 2:
                sleep(0.5)
            web_str = self.__get_web_str(word)
            data.append([web_str, self.__status_word])
            counter += 1
        return data

    # get from web solo word
    def __get_web_str(self, user_word):
        self.__status_word = True
        sleep(0.1)
        html = requests.get(
            "https://где-ударение.рф/в-слове-{}/".format(user_word.lower()))

        soup = BeautifulSoup(html.text, 'lxml')
        try:
            return soup.find("div", {"class": "rule"}).text.strip()
        except Exception as ex:
            self.__status_word = False
            return user_word

    def __get_accent(self, web_res):
        source_word = web_res.strip().split(' ')[-1][0:-1]
        word_accent = ''
        for letter in source_word:
            if letter in self.ACCENTS:
                letter = self.ACCENTS[letter]
            word_accent += letter
        return word_accent

    def one_word(self):
        try:
            first_word = self.answer_arr[0][0]
            if self.answer_arr[0][1]:
                description = ' '.join(first_word.strip().split(' ')[0:-1])
                acc_word = self.__get_accent(first_word)
                # output description and accent word
                return "{} {}.".format(description, acc_word)
            else:
                return 'Нет совпадений'
        except Exception as ex:
            return 'Нет совпадений'

    def many_words(self):
        b_words = ''
        ok_words = ''
        b_txt = 'По этим словам совпадений нет:'
        ok_txt = 'Ударения по текущим словам:'
        for word, status in self.answer_arr:
            if status:
                ok_words += '\n' + self.__get_accent(word)
            else:
                b_words += '\n' + word

        if len(b_words) == 0:
            return ok_txt + ok_words
        elif len(ok_words) == 0:
            return b_txt + b_words
        return ok_txt + ok_words + '\n' + b_txt + b_words
