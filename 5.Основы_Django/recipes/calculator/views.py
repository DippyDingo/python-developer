from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
}

# Напишите ваш обработчик. Используйте DATA как источник данных
# Результат - render(request, 'calculator/index.html', context)
# В качестве контекста должен быть передан словарь с рецептом:
# context = {
#   'recipe': {
#     'ингредиент1': количество1,
#     'ингредиент2': количество2,
#   }
# }
def recipe_view(request, recipe_name):
    # Ищем рецепт в словаре
    recipe = DATA.get(recipe_name)
    context = {}

    if recipe:
        # Ловим параметр servings из URL (если его нет, берем 1)
        servings = request.GET.get('servings', 1)

        # Переводим в число
        try:
            servings = int(servings)
        except ValueError:
            servings = 1

        # Умножаем граммовки и собираем новый словарь
        calculated_recipe = {}
        for ingredient, amount in recipe.items():
            calculated_recipe[ingredient] = round(amount * servings, 2)

        # Записываем результат в контекст
        context['recipe'] = calculated_recipe

    # Отдаем шаблон и контекст с данными
    return render(request, 'calculator/index.html', context)