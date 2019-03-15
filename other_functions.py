# Поиск в list условия перехода. Необходимо найти индекс.
import numpy as np

list_normal = [0, 0, 0, 0, 1]
list_work = [1, 1, 1, 1, 1]
list_not_work = [0, 0, 0, 0, 0]
list_debila_down = [0,1,0,0,1,0]
list_debila_up = [0,1,0,0,1,0,1]
list_shut = [1,1,1,1,0,0]
index_number = 0

print()
# print('Ненавижу матрицы!!!')
# True interface = down, False interface = up

list_check = np.array(list_normal)

x_list = np.nonzero(list_check!=0)[0]

# print(len(list_check))
if (len(list_check) == len(x_list)):
    print('interface work for all period')
elif  len(x_list) == 0:
    print('interface not work all period')
elif (list_check[-1] == 0):
    print('currently interface down')
    print('last up status, index',x_list[-1])
else:
    # Сравнить элементы пока неизвестно как
    print('currently interface up')
    t = x_list[0]
    if (min(list_check[t:]) == 0):
        print('currrently interface up, but swith up/down before')
    print('first status up, index =',t)
print()
    
    