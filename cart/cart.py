from decimal import Decimal
from django.conf import settings
from members.models import  Product, ProductShorts, ProductSneakers, ProductTshirt

class Cart(object):

    def __init__(self, request):
        """
        Инициализация корзины
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        print("Session Cart:", cart)  # Добавьте этот отладочный вывод
        if not cart:
            # сохраняем ПУСТУЮ корзину в сессии
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        print("Product IDs:", product_ids) 

        for product_id in product_ids:
            # Получаем элемент корзины
            item = self.cart[product_id]
            print("Item:", item)  # Отладочный вывод

            # Определяем модель продукта
            try:
                product = Product.objects.get(product_type=product_id)
                print("Product found in Product model")
            except Product.DoesNotExist:
                try:
                    product = ProductTshirt.objects.get(product_type=product_id)
                    print("Product found in ProductTshirt model")
                except ProductTshirt.DoesNotExist:
                    try:
                        product = ProductShorts.objects.get(product_type=product_id)
                    except ProductShorts.DoesNotExist:
                        try:
                            product = ProductSneakers.objects.get(product_type=product_id)
                        except ProductSneakers.DoesNotExist:
                            continue

            # Добавляем информацию о продукте к элементу корзины
            item['product'] = product
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']

            yield item


    def __len__(self):
        """
        Считаем сколько товаров в корзине
        """
        return sum(item['quantity'] for item in self.cart.values())


    def add(self, product, quantity=1, update_quantity=False):
        """
        Добавляем товар в корзину или обновляем его количество.
        """
        product_type = str(product.product_type)
        print("Product type:", product_type)  # Отладочный вывод

        if product_type not in self.cart:
            print("Product type not in cart")  # Отладочный вывод
            self.cart[product_type] = {'quantity': 0,
                                    'price': str(product.price)}
        else:
            print("Product type already in cart")  # Отладочный вывод

        if update_quantity:
            print("Updating quantity:", quantity)  # Отладочный вывод
            self.cart[product_type]['quantity'] = quantity
        else:
            print("Increasing quantity by:", quantity)  # Отладочный вывод
            self.cart[product_type]['quantity'] += quantity

        print("Cart contents after adding/updating product:", self.cart)  # Отладочный вывод

        self.save()


    def save(self):
        # сохраняем товар
        self.session.modified = True


    def remove(self, product):
        """
        Удаляем товар
        """
        product_type = str(product.product_type)
        if product_type in self.cart:
            del self.cart[product_type]
            self.save()


    def remove_all(self):
        
        self.cart.clear()
        self.save()


    def get_total_price(self):
        # получаем общую стоимость
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())


    def clear(self):
        # очищаем корзину в сессии
        del self.session[settings.CART_SESSION_ID]
        self.save()


