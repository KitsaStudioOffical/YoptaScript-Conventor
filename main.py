import re

def load_dictionary(filepath):
    dictionary = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()  # читаем все строки из файла
        for line in lines:  # перебираем все строки
            if "['" in line and "']" in line:  # ищем строки с массивом
                parts = line.split("['")[1].split("', '")  # разделяем по элементам
                if len(parts) == 2:  # если нашли два элемента
                    key = parts[0].strip()  # берем первый элемент как ключ
                    value = parts[1].strip().strip("'],")  # второй как значение
                    dictionary[key] = value  # добавляем в словарь
    return dictionary  # возвращаем словарь

def js_to_yopta(js_code, dictionary):
    # Заменяем только ключевые слова но не строки
    def replacer(match):
        word = match.group(0)  # получаем найденное слово
        if word in dictionary:  # если слово есть в словаре
            return dictionary[word]  # возвращаем замену из словаря
        return word  # если нет, возвращаем слово как есть

    # Регулярное выражение для поиска ключевых слов
    js_code = re.sub(r'\b(?:' + '|'.join(re.escape(key) for key in dictionary.keys()) + r')\b', replacer, js_code)
    return js_code  # возвращаем измененный код

def convert_js_to_yopta(js_filepath, yopta_filepath, dictionary):
    with open(js_filepath, 'r', encoding='utf-8') as js_file:
        js_code = js_file.read()  # читаем весь код из js файла

    yopta_code = js_to_yopta(js_code, dictionary)  # конвертируем в yoptaScript

    with open(yopta_filepath, 'w', encoding='utf-8') as yopta_file:
        yopta_file.write(yopta_code)  # записываем результат в новый файл

dictionary_path = 'dictionary.ts'  # путь к словарю
dictionary = load_dictionary(dictionary_path)  # загружаем словарь

js_filepath = 'script.js'  # путь к исходному файлу
yopta_filepath = 'script.ys'  # путь к выходному файлу

convert_js_to_yopta(js_filepath, yopta_filepath, dictionary)  # конвертируем

print(f"YoptaScript код сохранен в {yopta_filepath}")  # выводим сообщение
