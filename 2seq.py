num_str = input('\nВведите любые цифры через запятую: ')
my_list = num_str.split(',')
new_list = list(set(my_list))
print('\nНовый список уникальных элементов:\n', new_list)
