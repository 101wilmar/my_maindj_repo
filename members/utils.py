
import random

from .models import Action


class DataMixin: 
  def get_mixin_context(self, context, **kwargs):
    context.update(kwargs)



def recommend_products(user, current_product):
    recommend_prod = set()  # Множество для хранения уникальных товаров
    user_actions = Action.objects.filter(user=user)
    product_user = [(action.product_type, action.product_id) for action in user_actions]

    # Получаем цвет текущего просматриваемого товара
    current_color = current_product.color

    # Определяем модель текущего продукта
    product_model = current_product.__class__

    # Получаем все товары с таким же цветом, исключая текущий продукт и просмотренные пользователем товары
    similar_products = product_model.objects.filter(color=current_color)
    similar_products = similar_products.exclude(id=current_product.id)
    similar_products = similar_products.exclude(id__in=[product_id for product_type, product_id in product_user])

    # Добавляем похожие товары в список рекомендаций
    recommend_prod.update(similar_products)

    # Проверяем, нужно ли дополнить список случайными товарами
    while len(recommend_prod) < 5:
        # Получаем случайные товары
        random_products = product_model.objects.all()
        random_products = random_products.exclude(id=current_product.id)
        random_products = random_products.exclude(id__in=[product_id for product_type, product_id in product_user])
        
        # Фильтруем случайные товары, чтобы оставить только уникальные
        unique_random_products = [product for product in random_products if product not in recommend_prod]

        # Если нет уникальных случайных товаров для добавления, выходим из цикла
        if not unique_random_products:
            break
        
        # Определяем количество товаров, которые нужно добавить
        remaining = 5 - len(recommend_prod)
        
        # Если количество уникальных случайных товаров меньше или равно оставшемуся количеству, добавляем все доступные
        if len(unique_random_products) <= remaining:
            recommend_prod.update(unique_random_products)
            break
        
        # Добавляем уникальные случайные товары, пока не достигнем нужного количества
        random_selection = random.sample(unique_random_products, remaining)
        recommend_prod.update(random_selection)

    print('Rec', recommend_prod)
    return list(recommend_prod) 
