import time
import telebot as tb
import string
from pymystem3 import Mystem
from random import randint
from bs4 import BeautifulSoup
import requests

bot = tb.TeleBot('5847056034:AAEtCBn0HP9IsxPO92qhvsVZOxUzNkolDmc')
tmp = 0

""" Приведение к начальной форме и удаление символов пунктуации """


def remove_punctuation_and_diction_form(text):
    m = Mystem()
    text = ''.join(m.lemmatize(text)).rstrip('\n')

    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)


""" Чтение информации из текстовых файлов в датасеты(list) """
countries_nonready_dataset, questions_dataset, countries_info = [], [], []


def Read_In_Data(filename, datalist):
    f = open(f"./{filename}", "r")

    for i in f:
        datalist.append(i.rstrip('\n'))


Read_In_Data('countries', countries_nonready_dataset)
Read_In_Data('question_words', questions_dataset)

""" В файле countries первый элемент строки - преобразованное название страны, второй - нормальное ее название """
countries_dataset, countries_dataset2 = [], []
for i in countries_nonready_dataset:
    c = i.split()
    countries_dataset.append(c[0])  # страны в начальной форме
    countries_dataset2.append(c[1])  # страны обычные

key_words = {
    'mountains': {  # горы
        'Китай',
        'Индия',
        'Австрия',
        'Испания',
        'Италия',
        'США',
        'Франция',
        'Турция'
    }, 'sand': {  # пустыни
        'Греция',
        'Индия',
        'Италия',
        'Испания',
        'США',
        'ОАЭ',
        'Египет'
    }, 'nature': {  # природа
        'Мексика',
        'Китай',
        'США',
        'Мексика',
        'Австрия'
    }, 'castles': {  # замки
        'Германия',
        'Великобритания',
        'Франция',
        'Нидерланды',
        'Испания',
        'Португалия'
    }, 'ancient': {  # древние постройки
        'Камбоджа',
        'Мексика',
        'Индия',
        'Италия',
        'Швейцария'
    }, 'diving': {  # дайвинг
        'Австрия',
        'Франция',
        'ОАЭ',
        'Турция',
        'Греция'
    }, 'clubs': {  # клубы
        'Испания',
        'Италия',
        'Греция',
        'США',
        'ОАЭ',
        'Швейцария'
    }, 'family': {  # семейный отдых
        'Турция',
        'Испания',
        'ОАЭ',
        'Греция'
    }, 'skis': {  # лыжи
        'Австрия',
        'Германия',
        'Италия',
        'Китай',
        'Швейцария'
    }, 'seas': {
        'Великобритания',
        'Германия',
        'Греция',
        'Израиль',
        'Индия',
        'Испания',
        'Италия',
        'Камбоджа',
        'Китай',
        'Мексика',
        'Нидерланды',
        'Финляндия',
        'Франция',
        'Турция'
    }, 'oceans': {
        'Великобритания',
        'Индия',
        'Испания',
        'Камбоджа',
        'Мексика',
        'Португалия',
        'США',
        'Франция',
        'ОАЭ'
    }, 'kitchen': {
        'Великобритания',
        'Индия',
        'Испания',
        'США',
        'Франция',
        'ОАЭ',
        'Финляндия',
        'Греция',
        'Швейцария'
    }

}
""" 
-записываем все страны в файл other_countries
page_countries = requests.get('https://ru.wikipedia.org/wiki/Список_государств')
soup_countries = BeautifulSoup(page_countries.text, "html.parser")
file = open('./other_countries', 'w')
def Generation_countries_out_file():
    tr = soup_countries.findAll('a')
    c, s = 0, []
    for a in tr: # 36-420
        c += 1
        if 36 <= c <= 420 and c % 2 == 0:
            file.write(f'{remove_punctuation_and_diction_form(a.text)} ')
            file.write(f'{a.text}\n')
    file.close()
Generation_countries_out_file()
"""


def other_countries_reading():  # читаем все страны в s
    file = open('other_countries', 'r')
    s = []
    for cntr in file:
        s.append(cntr.rstrip('\n'))
    return s


# print(other_countries_reading())

def sample_reply_key_words(return_message, word, key_words2):
    return_message = ''
    list_samples = [
        'Хотите окунуться в ',
        'Итак, нас интересует ',
        'Что может быть лучше, чем ',
        'Как прекрасен ',
        'Большую популярность сейчас набирает ',
        'Одно из самых популярных направлений отдыха: ',
        'Ваш выбор пал на '
    ]
    list_samples2 = [
        'Перечень стран, обладающих ',
        'Список стран, обладающих ',
        'Страны, обладающие ',
        'Вот страны, располагающие ',
        'Весь перечень стран, располагающих ',
        'Несколько стран, располагающих ',
        'Страны, располагающие '

    ]
    return_message += list_samples[randint(0, len(list_samples) - 1)]
    return_message += f'{word}! '
    return_message += f'{list_samples2[randint(0, len(list_samples2) - 1)]}{key_words2}: '
    return f'{return_message}'


def print_countries_after_sample(return_message, key):
    counter, tmp_c = len(key), 0
    for cm in key:  # забегаем в key_words['key'] и каждую страну добавляем
        return_message += f'{cm}'
        tmp_c += 1
        if tmp_c == counter:
            break
        return_message += ', '
    return f'{return_message}. '


""" Тесты """
message1 = "привет, бот. дай мне список стран с морями а так же лыжи есть поесть"
correct_m = remove_punctuation_and_diction_form(message1)
# print(correct_m)
list_words_m = correct_m.split()


def comparison_main_message(list_words_m):  # совпадения стран
    count, oz_count = 0, 0
    list_countries_in_message = []
    hotel_country = False
    return_message = ''
    flag_answer = 0

    for word in range(len(list_words_m)):  # главный цикл перебора слов в сообщении
        for country in range(len(countries_dataset)):  # цикл перебора стран в списке со странами
            if list_words_m[word] == countries_dataset[country]:
                list_countries_in_message.append(country)
                count += 1
        if (list_words_m[word]) == 'отель':
            hotel_country = True

        ocr = other_countries_reading()  # список со всеми странами

        if list_words_m[word] == 'привет' or list_words_m[word] == 'здравствовать' or \
                list_words_m[word] == 'здаров' or list_words_m[word] == 'здоров' or \
                list_words_m[word] == 'хай' or list_words_m[word] == 'хей' or \
                list_words_m[word] == 'приветствовать' or list_words_m[word] == 'ку':
            return_message = hello_answer()
        if list_words_m[word] == 'хорошо' or list_words_m[word] == 'спасибо' or \
                list_words_m[word] == 'ока' or list_words_m[word] == 'окей' or \
                list_words_m[word] == 'принятый' or list_words_m[word] == 'отлично' or \
                list_words_m[word] == 'понятно' or list_words_m[word] == 'окать':
            return_message = OK_answer()
        for cntr in range(len(ocr)):
            if list_words_m[word] == ocr[cntr].split()[0] and count == 0:
                return_message = f'В моем списке туристических стран страны "{ocr[cntr].split()[1]}" страны пока нет.\n'
        if list_words_m[word] == 'море' or list_words_m[word] == 'морской' or list_words_m[word] == 'купаться':
            return_message += sample_reply_key_words(return_message, 'отдых на море',
                                                     'чистыми и прозрачными морями')
            return_message = print_countries_after_sample(return_message, key_words['seas'])
            return_message += 'Какая(ие) из этих стран Вас интересуют?\n'
            flag_answer = 1
            break
        elif list_words_m[word] == 'океан' or list_words_m[word] == 'океанский':
            return_message += sample_reply_key_words(return_message, 'отдых на берегу океана',
                                                     'глубокими и бесконечно далекими океанами')
            return_message = print_countries_after_sample(return_message, key_words['oceans'])
            return_message += 'Какая(ие) из этих стран Вас интересуют?\n'
            flag_answer = 2
            break
        elif list_words_m[word] == 'гора' or list_words_m[word] == 'возвышенность' or list_words_m[word] == 'горный':
            return_message += sample_reply_key_words(return_message, 'отдых в горах',
                                                     'пленяющими видами и возвышенностями')
            return_message = print_countries_after_sample(return_message, key_words['mountains'])
            return_message += 'Какая(ие) из этих стран Вас интересуют?\n'
            flag_answer = 3
            break
        elif list_words_m[word] == 'пустыня' or list_words_m[word] == 'песок' or list_words_m[word] == 'пустынный':
            return_message += sample_reply_key_words(return_message, 'отдых с пустынями',
                                                     'завораживающими пустынными дюнами и песочными полями')
            return_message = print_countries_after_sample(return_message, key_words['sand'])
            return_message += 'Какая(ие) из этих стран Вас интересуют?\n'
            flag_answer = 4
            break
        elif list_words_m[word] == 'природа' or list_words_m[word] == 'пейзаж' or list_words_m[word] == 'природный':
            return_message += sample_reply_key_words(return_message, 'отдых на природе',
                                                     'прекрасной экологией красивой природой')
            return_message = print_countries_after_sample(return_message, key_words['nature'])
            return_message += 'Какая(ие) из этих стран Вас интересуют?\n'
            flag_answer = 5
            break
        elif list_words_m[word] == 'замок' or list_words_m[word] == 'крепость':
            return_message += sample_reply_key_words(return_message, 'путешествие по замкам и крепостям',
                                                     'величественными замками и древними крепостями')
            return_message = print_countries_after_sample(return_message, key_words['castles'])
            return_message += 'Какая(ие) из этих стран Вас интересуют?\n'
            flag_answer = 6
            break
        elif list_words_m[word] == 'древность' or list_words_m[word] == 'древний':
            return_message += sample_reply_key_words(return_message, 'путешествие по древностям',
                                                     'интересными историческими достопримечательностями')
            return_message = print_countries_after_sample(return_message, key_words['ancient'])
            return_message += 'Какая(ие) из этих стран Вас интересуют?\n'
            flag_answer = 7
            break
        elif list_words_m[word] == 'подводный' or list_words_m[word] == 'дайвинг' or list_words_m[word] == 'вода':
            return_message += sample_reply_key_words(return_message, 'дайвинг',
                                                     'глубокими подводными впадинами и ущельями')
            return_message = print_countries_after_sample(return_message, key_words['diving'])
            return_message += 'Какая(ие) из этих стран Вас интересуют?\n'
            flag_answer = 8
            break
        elif list_words_m[word] == 'клуб' or list_words_m[word] == 'тусовка' or list_words_m[word] == 'весело' or \
                list_words_m[word] == 'веселиться' or list_words_m[word] == 'оторваться':
            return_message += sample_reply_key_words(return_message, 'активный отдых с тусовками',
                                                     'классными клубами и развлекательными программами')
            return_message = print_countries_after_sample(return_message, key_words['clubs'])
            return_message += 'Какая(ие) из этих стран Вас интересуют?\n'
            flag_answer = 9
            break
        elif list_words_m[word] == 'семья' or list_words_m[word] == 'дети' or list_words_m[word] == 'родители' \
                or list_words_m[word] == 'семейный':
            return_message += sample_reply_key_words(return_message, 'уютный семейный отдых',
                                                     'отличными семейными отелями и условиями для близкого круга')
            return_message = print_countries_after_sample(return_message, key_words['family'])
            return_message += 'Какая(ие) из этих стран Вас интересуют?\n'
            flag_answer = 10
            break
        elif list_words_m[word] == 'лыжа' or list_words_m[word] == 'лыжный' or list_words_m[word] == 'горнолыжный':
            return_message += sample_reply_key_words(return_message, 'лыжный отдых',
                                                     'экстремальными горными спусками и трамплинами')
            return_message = print_countries_after_sample(return_message, key_words['skis'])
            return_message += 'Какая(ие) из этих стран Вас интересуют?\n'
            flag_answer = 11
            break
        elif list_words_m[word] == 'кухня' or list_words_m[word] == 'морепродукт' or list_words_m[word] == 'вкусно' \
                or list_words_m[word] == 'еда' or list_words_m[word] == 'поесть':
            return_message += sample_reply_key_words(return_message, 'экзотическая еда',
                                                     'богатыми кухнями и разнообразными угощениями')
            return_message = print_countries_after_sample(return_message, key_words['kitchen'])
            return_message += 'Какая(ие) из этих стран Вас интересуют?\n'
            flag_answer = 12
            break

    return_country = []
    if count == 1:  # если указана одна страна
        return_country.append(countries_dataset2[list_countries_in_message[0]])
        if hotel_country:  # если есть "отель"
            return_message += f'Хотите подобрать отель в стране {countries_dataset2[list_countries_in_message[0]]}?\n'
            flag_answer = 13
        else:
            return_message += f'Хотите узнать про страну {countries_dataset2[list_countries_in_message[0]]}?\n'
            flag_answer = 14

    elif count > 1:  # если указано несколько стран
        if hotel_country:  # если есть "отель"
            return_message += 'Хотите подобрать отель в странах: '
            for word in range(count):
                return_country.append(countries_dataset2[list_countries_in_message[word]])
                return_message += countries_dataset2[list_countries_in_message[word]]
                if word == count - 1:
                    break
                return_message += ', '
            return_message += '?\n'
            flag_answer = 15
        else:
            return_message += 'Хотите узнать про страны: '
            tmp_c = 0
            for word in range(count):
                return_country.append(countries_dataset2[list_countries_in_message[word]])
                return_message += countries_dataset2[list_countries_in_message[word]]
                tmp_c += 1
                if tmp_c == count:
                    break
                return_message += ', '
            return_message += '?\n'
            flag_answer = 16

    if return_message == '':  # откат
        return 'Я не знаю что на это ответить. Составьте предложение более корректно.\n'
    else:
        return return_message, flag_answer, return_country


# print(comparison_main_message(correct_m))

def comparison_second_message(list_words_m2):  # второе сообщение
    second_message = remove_punctuation_and_diction_form(list_words_m2)


# нужна проверка на (хочу / не _ хочу)

# ключевые слова: аквапарки, кухня, дети, название_моря, храмы, джунгли, экзотика,
# вечеринки, морепродукты


@bot.message_handler(commands=['start'])
def Command_Start(message):
    bot.send_message(message.chat.id, 'Привет! Я ии-гид. В своем сообщении уточните, в какой бы стране вы хотели '
                                      'побывать, или что должен включать в себя курорт, например:\nдайвинг, горнолыжный'
                                      ' курорт, природа, семейный отдых, клубы, горы, древние постройки, пустыни '
                                      'или замки.\n')


s13, s14, s15, s16, s16_1, c16 = [], [], [], [], [], 0


def list_maker(list_, part):  # закидываем страну part в list_ список
    list_.clear()
    list_.append(part)



@bot.message_handler(content_types=['text'])
def first_answer(message):
    global c16
    c16 = 0
    message_text_bot = message.text
    correct_message_bot = remove_punctuation_and_diction_form(message_text_bot)
    print(correct_message_bot)
    list_words_m_bot = correct_message_bot.split()
    var = comparison_main_message(list_words_m_bot)[1]
    # print(comparison_main_message(list_words_m_bot))
    tmp14_1 = '-'
    for word in list_words_m_bot:  # проверяем сообщение на наличие стран
        for country in countries_dataset:
            if word == country:
                c16 += 1
                tmp14_1 = word
    # print(c16)
    list_maker(s14, tmp14_1)
    tmp14 = '--'
    for cntr in range(len(countries_dataset)):  # ищем страну в списке countries_dataset и вставляем в s14 ее название
        if s14[0] == countries_dataset[cntr]:
            tmp14 = countries_dataset2[cntr]
    list_maker(s14, tmp14)
    for word in list_words_m_bot:
        for country in countries_dataset:
            if word == country:
                s16.append(word)
    # print(s16)
    for word in s16:
        for country in range(len(countries_dataset)):
            if word == countries_dataset[country]: s16_1.append(
                countries_dataset2[country])  # формируем список стран 16
    # print(s16_1)
    bot.send_message(message.chat.id, comparison_main_message(list_words_m_bot))

    if var == 77:
        bot.register_next_step_handler(message, hello_answer)
    if var == 13:  # страна+отель
        bot.register_next_step_handler(message, answer13)
    if var == 14:  # страна
        bot.register_next_step_handler(message, answer14)
    elif var == 15:  # страны+отель
        bot.register_next_step_handler(message, answer15)
    elif var == 16:  # страны
        bot.register_next_step_handler(message, answer16)


def create_info_about_country():
    file = open('countries_info_a', 'r')
    container, container1 = [], []

    for string_f in file:
        container.append(string_f.split())

    return container


def split_and_reg_parts(string_info: str):
    s = string_info.split(':')

    return s


def hello_answer():
    hello_list = [
        'Привет-привет! ',
        'Ха-ха, привет) ',
        'Еще раз здравствуйте ',
        'Приветик. ',
        'Да, здравствуй. ',
        'Ку-ку! '
    ]
    return_message = hello_list[randint(0, 5)]
    return return_message

def OK_answer():
    ok_list = [
        'Обращайтесь! ',
        'Отдыхайте! ',
        'Бывайте! ',
        'Приятного отдыха! ',
        ';) '
    ]
    return_message = ok_list[randint(0, 5)]
    return return_message


def answer13(message):
    return_message = ''
    country = s14[0]
    index = countries_dataset.index(remove_punctuation_and_diction_form(country))
    added = create_info_about_country()
    added_str = ''
    for word in added[index]:
        added_str += word
        added_str += ' '
    return_message += f'Информация об отелях страны {country}:\n'
    return_message += f'Самый недорогой отель в стране: {split_and_reg_parts(added_str)[8]} (цена за сутки)\n' \
                      f'Отель среднего бюджета: {split_and_reg_parts(added_str)[9]} (цена за сутки)\n' \
                      f'Самый дорогой и престижный отель: {split_and_reg_parts(added_str)[10]} (цена за сутки).\n\n'
    bot.send_message(message.chat.id, return_message)


def answer14(message):  # какая-либо страна
    cor_message_text = remove_punctuation_and_diction_form(message.text)
    if ('да' in cor_message_text or 'конечно' in cor_message_text or 'хотеть' in cor_message_text or 'можно'
        in cor_message_text or 'давать' in cor_message_text) and ('не' not in cor_message_text):
        # обработчик сообщений после страны
        return_message, country = '', s14[0]
        index = countries_dataset.index(remove_punctuation_and_diction_form(country))
        added = create_info_about_country()
        added_str = ''
        for word in added[index]:
            added_str += word
            added_str += ' '
        seas = f'Моря, омывающие эту страну: {split_and_reg_parts(added_str)[4]}'
        oceans = f'Океаны, омывающие эту страну: {split_and_reg_parts(added_str)[2]}'
        temp = f'Средние температуры в старне: {split_and_reg_parts(added_str)[6]}'
        hotels = f'Три лучших отеля по различным ценам: {split_and_reg_parts(added_str)[8]}, ' \
                 f'{split_and_reg_parts(added_str)[9]}, {split_and_reg_parts(added_str)[10]}'
        if 'никакие' in split_and_reg_parts(added_str)[4]: seas = 'Никакие моря не омывают эту страну'
        if 'никакие' in split_and_reg_parts(added_str)[2]: oceans = 'Никакие океаны не омывают эту страну'

        return_message_14 = f'Информация про страну {split_and_reg_parts(added_str)[0]}:\n' \
                            f'{oceans};\n{seas};\n{temp};\n{hotels}.\n\n'
        bot.send_message(message.chat.id, return_message_14)
    else:
        bot.send_message(message.chat.id, 'Что ж, продолжим общение на другую тему!')


def answer15(message):  # страны и отель
    return_message = ''
    tmp_c = 0
    s16_1.reverse()
    s16.reverse()
    for country_in_s16_1 in range(len(s16_1)):
        index = countries_dataset.index(s16[country_in_s16_1])
        added = create_info_about_country()
        added_str = ''
        for word in added[index]:
            added_str += word
            added_str += ' '

        return_message += f'Информация об отелях страны {s16_1[country_in_s16_1]}:\n'
        return_message += f'Самый недорогой отель в стране: {split_and_reg_parts(added_str)[8]} (цена за сутки)\n' \
                          f'Отель среднего бюджета: {split_and_reg_parts(added_str)[9]} (цена за сутки)\n' \
                          f'Самый дорогой и престижный отель: {split_and_reg_parts(added_str)[10]} (цена за сутки).\n\n'

        tmp_c += 1
        if tmp_c == c16:  ##
            break
    bot.send_message(message.chat.id, return_message)


def answer16(message):  # страны
    cor_message_text = remove_punctuation_and_diction_form(message.text)
    if ('да' in cor_message_text or 'конечно' in cor_message_text or 'хотеть' in cor_message_text or 'можно'
        in cor_message_text or 'давать' in cor_message_text) and ('не' not in cor_message_text):
        return_message_16 = ''
        tmp_c, counter = 0, len(s16_1)
        s16_1.reverse()
        s16.reverse()
        global c16
        print(s16_1, s16)
        for country_in_s16_1 in range(len(s16_1)):
            index = countries_dataset.index(s16[country_in_s16_1])
            added = create_info_about_country()
            added_str = ''
            for word in added[index]:
                added_str += word
                added_str += ' '

            seas = f'Моря, омывающие эту страну: {split_and_reg_parts(added_str)[4]}'
            oceans = f'Океаны, омывающие эту страну: {split_and_reg_parts(added_str)[2]}'
            temp = f'Средние температуры в старне: {split_and_reg_parts(added_str)[6]}'
            hotels = f'Три лучших отеля по различным ценам: {split_and_reg_parts(added_str)[8]}, ' \
                     f'{split_and_reg_parts(added_str)[9]}, {split_and_reg_parts(added_str)[10]}r'
            if 'никакие' in split_and_reg_parts(added_str)[4]: seas = 'Никакие моря не омывают эту страну'
            if 'никакие' in split_and_reg_parts(added_str)[2]: oceans = 'Никакие океаны не омывают эту страну'

            return_message_16 += f'Информация про страну {split_and_reg_parts(added_str)[0]}:\n' \
                                 f'{oceans};\n{seas};\n{temp};\n{hotels}.\n\n'
            tmp_c += 1
            if tmp_c == c16:  ##
                break
        bot.send_message(message.chat.id, return_message_16)
        s16_1.clear()
        s16.clear()
    else:
        bot.send_message(message.chat.id, 'Что ж, продолжим общение на другую тему!')
        s16_1.clear()
        s16.clear()


bot.polling(none_stop=True)
# while True:
#     try:
#         bot.polling(none_stop=True)
#
#     except Exception as e:
#         print(e)
#         time.sleep(15)
