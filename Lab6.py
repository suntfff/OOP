data = {
    'numbers':[1, 2, 3, 4, 5, 6, 7, 8], 
    'searching_number': 6, 
    'len_numbers': 0, 
    'right': 0, 
    'left': 0, 
    'middle': 0
}

i = 0
while True:
    try:
        data['numbers'][i]
        i+=1
    except:
        break

data['len_numbers'] = i
data['right'] = data['len_numbers'] - 1

while data['right'] >= data['left']:
    data['middle'] = (data['left'] + data['right']) // 2
    if data['numbers'][data['middle']] > data['searching_number']:
        data['right'] = data['middle'] + 1
    elif data['numbers'][data['middle']] < data['searching_number']:
        data['left'] = data['middle'] - 1
    else:
        print(data['middle'])
        break
else:
    print('Элемент не найден')
