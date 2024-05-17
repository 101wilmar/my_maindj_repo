from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from members.models import Product, ProductShorts, ProductSneakers, ProductTshirt
from .cart import Cart
from .forms import CartAddProductForm
from django.contrib.auth.decorators import login_required


@require_POST
def cart_add(request, product_type):
    cart = Cart(request)
    
    # Попытка найти продукт в модели Product
    try:
        product = Product.objects.get(product_type=product_type)
    except Product.DoesNotExist:
        # не найдено, попытка найти продукт в модели ProductTshirt
        try:
            product = ProductTshirt.objects.get(product_type=product_type)
        except ProductTshirt.DoesNotExist:
            # не найдено, попытка найти продукт в модели ProductShorts
            try:
                product = ProductShorts.objects.get(product_type=product_type)
            except ProductShorts.DoesNotExist:
                # попытка найти продукт в модели ProductSneakers      
                try:
                    product = ProductSneakers.objects.get(product_type=product_type)
                except ProductSneakers.DoesNotExist:
                    return JsonResponse({'success': False, 'message': 'Product not found.'})

    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
        return JsonResponse({'success': True, 'message': 'Product added to cart.'})
    return JsonResponse({'success': False, 'message': 'Invalid form data.'})

 
def cart_remove(request, product_type):
    cart = Cart(request)
    
    # Попытка найти продукт в модели Product
    try:
        product = Product.objects.get(product_type=product_type)
    except Product.DoesNotExist:
        # Если не найдено, попытка найти продукт в модели ProductTshirt
        try:
            product = ProductTshirt.objects.get(product_type=product_type)
        except ProductTshirt.DoesNotExist:
            # Если не найдено, попытка найти продукт в модели ProductShorts
            try:
                product = ProductShorts.objects.get(product_type=product_type)
            except ProductShorts.DoesNotExist:
                try:
                    product = ProductSneakers.objects.get(product_type=product_type)
                except ProductSneakers.DoesNotExist:
                    return JsonResponse({'success': False, 'message': 'Product not found.'})

    cart.remove(product)
    return redirect('cart:cart_detail')


def clear_cart(request):
    cart = Cart(request)
    cart.remove_all()
    print("Cart cleared successfully")   # Отладочное сообщение
    return redirect('cart:cart_detail')


@login_required
def cart_detail(request):
    cart = Cart(request)
    cart_quantity = len(cart)

    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'update': True})
    return render(request, 'cart/detail.html', {'cart': cart, 'cart_quantity': cart_quantity})
