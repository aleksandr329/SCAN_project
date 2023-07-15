import json
import nltk
import string
import pymorphy3  # для обработки слова "стали" в "стать"
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')


spec_chars = string.punctuation + '\n\xa0«»\t—…'
morph = pymorphy3.MorphAnalyzer()


def lowercase_text(text):
    text = "".join([ch for ch in text if ch not in spec_chars])                            #Убираем пунктуацию
    low_text = text.lower()                                                                # в нижний регистр
    delete_text = ''.join(low_text)                                                        #получаем обратно строку
    text_tokens = word_tokenize(delete_text)                                               #делим строку обратно на слова
    tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]    #убираем ненужные слова из списка
    without_sw_on_str = ' '.join(tokens_without_sw)                                        #делаем из списка строку
    without_sw_on_list = word_tokenize(without_sw_on_str)                                  #делим строку обратно на слова
    words = without_sw_on_list                                                             # функция убираем стоп слова
    parsed_words = [morph.parse(word) for word in words]                                   # (в этом списке 151 слово)
    normal_forms = [word[0].normal_form for word in parsed_words]                          # пример: и, в, во, \
    return normal_forms                                                                    # получаем список слов ключевых


with open('cloud.json', 'r', encoding='utf-8')as f:
    text = json.load(f)


def examination(spisok):
    try:
        new_list = []
        for i in range(len(text)):                  #При помощи этого цикла мы можем проитерировать весь список [text]
            count = 0                               #благодоря функции range(в которой функция len) мы автоматически определяем
            cycle_list = []                         #длинну этого списка
            for s in text[i]["WordCloud"]:          #При помощи этого цикла мы итерируем словари по ключам "WordCloud"
                if s in spisok:                     #И если есть совпадение делаем следующию логику
                    count += 1
                    if i not in cycle_list:
                        cycle_list.append(i)
            else:                                   #После цикла 2-ого for мы применяем оператор else который формирует новый список
                if count > 0:                       #если он не нулевой
                    cycle_list.append(count)
                    new_list.append(cycle_list)

        t = max(new_list, key=lambda i: i[1])      #Благодоря функции lambda мы проходим по нашим новым спискам и вычисляем где
        result = [text[t[0]]["Theme"], text[t[0]]["cat"]]              #было больше всего совпадений в нашем облаке.

    except ValueError:
        result = 'К сожаление наш БОТ не нашел ничего по вашему запросу ☹, пожалуйста введите другой запрос!'
        return result

    return result
