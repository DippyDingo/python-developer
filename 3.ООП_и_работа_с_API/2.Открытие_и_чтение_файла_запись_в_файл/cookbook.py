def read (reading_file):
    cook_book = {}
    with open(reading_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue
            dish_name = line
            i += 1
            ingredients_count = int(lines[i].strip())
            i += 1

            ingredients = []
            for _ in range(ingredients_count):
                ingredient_line = lines[i].strip()
                name, quantity, measure = [x.strip() for x in ingredient_line.split('|')]

                ingredients.append({
                    'name': name,
                    'quantity': int(quantity),
                    'measure': measure
                })
                i += 1
            cook_book[dish_name] = ingredients
    return cook_book

def get_list(dish_list, person_count, cook_book):
    shop_list = {}
    for dish in dish_list:
        if dish not in cook_book:
            print(f'Блюдо "{dish}" отсутствует в кулинарной книге.')
            continue
        ingredients = cook_book[dish]
        for ingredient in ingredients:
            name = ingredient['name']
            quantity = ingredient['quantity'] * person_count
            measure = ingredient['measure']

            if name in shop_list:
                shop_list[name]['quantity'] += quantity
            else:
                shop_list[name] = {
                    'measure': measure,
                    'quantity': quantity
                }
    return shop_list

cook = read('recipes.txt')
list_dish = get_list(['Омлет'], 2, cook)
print(list_dish)

