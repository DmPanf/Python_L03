import random

people = {'М.В. Ломоносова': '19.11.1711', 'С.В. Ковалевской': '15.01.1850', 'А.С. Пушкина': '06.06.1799',
          'Д.И. Менделеева': '08.02.1834', 'Ю.А. Гагарина': '09.03.1934', 'Стива Джобса': '24.02.1955',
          'Джека Лондона': '12.01.1876', 'С.П. Королева': '12.01.1907', 'Исаака Ньютона': '04.01.1643',
          'Алана Тьюринга': '23.06.1936', }
day_word = {'19': 'девятнадцатого', '15': 'пятнадцатого', '06': 'шестого', '08': 'восьмого', '09': 'девятого',
            '24': 'двадцать четвертого', '12': 'двенадцатого', '04': 'четвертого', '23': 'двадцать третьего'}
month_word = {'11': 'ноября', '01': 'января', '06': 'июня', '02': 'февраля', '03': 'марта'}
sample_people = random.sample(list(people), 5)
correct_answers = 0
wrong_answers = 0


def data_to_word(name):
    str_data = ''
    data = people[name]
    str_data += day_word[data[:2]] + ' '
    str_data += month_word[data[3:5]] + ' '
    str_data += data[6:10] + ' года'
    return str_data


print('\nВам нужно будет вводить даты рождения известных людей в формате [dd.mm.yyyy].')
for person in sample_people:
    new_data = input(f'\nВведите дату рождения {person}: ')
    word = data_to_word(person)
    if new_data == people[person]:
        correct_answers += 1
    else:
        print(f'... дата рождения {person}: {word}!')
        wrong_answers += 1

print(f'\n✅ количество правильных ответов: {correct_answers} [{round((correct_answers * 100) / 5, 0)} %] из 5')
print(f'❌ количество ошибок: {wrong_answers} [{round((wrong_answers * 100) / 5, 0)} %] из 5')
