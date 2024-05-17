
from django.views import View
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse
from django.template import loader

from django.core.cache import cache
from django.utils.http import urlencode
from cart.cart import Cart
from .utils import recommend_products
from .models import  Product, Category, ProductShorts, ProductSneakers, ProductTshirt
from cart.forms import CartAddProductForm
from .forms import ColorFilterForm, PaySystemForm
from django.db.models import Q


def members(request):
  template = loader.get_template('all_members.html')
  return HttpResponse(template.render())


def product_detail(request, id, slug, model, template_name):
    product = get_object_or_404(model, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    cart_product_form = CartAddProductForm()
    user = request.user
    
    # Передаем информацию о текущем продукте в функцию рекомендаций
    recommended_products = recommend_products(user, product)
    return render(request, template_name, {
        'product': product,
        'cart_product_form': cart_product_form,
        'recommended_products': recommended_products,
    })

def product_detail_product(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    return product_detail(request, id, slug, Product, 'detail.html')

def product_detail_product_tshirt(request, id, slug):
    product = get_object_or_404(ProductTshirt, id=id, slug=slug, available=True)
    return product_detail(request, id, slug, ProductTshirt, 'product_detail_thirt.html')

def product_detail_shorts(request, id, slug):
    product = get_object_or_404(ProductShorts, id=id, slug=slug, available=True)
    return product_detail(request, id, slug, ProductShorts, 'product_detail_shorts.html')

def product_detail_sneakers(request, id, slug):
    product = get_object_or_404(ProductSneakers, id=id, slug=slug, available=True)
    return product_detail(request, id, slug, ProductSneakers, 'product_detail_sneakers.html')


class ShopListView(ListView):
    context_object_name = 'products'
    template_name = 'shop.html'
    model = Product
    paginate_by = 9  

    def get_queryset(self):
        selected_brands = self.request.GET.getlist('category')
        selected_color = self.request.GET.getlist('color')
        max_price = self.request.GET.get('price_max')
        min_price = self.request.GET.get('price_min')
        direction = self.request.GET.get('direction')


        cache_key = f"product:{urlencode(self.request.GET)}"
        queryset = cache.get(cache_key)

        if queryset is None:  # Используем `is None`, чтобы убедиться, что queryset не закэширован
            queryset = Product.objects.filter(available=True)
            # Фильтрация по брендам
            if selected_brands:
                queryset = queryset.filter(category__name__in=selected_brands)

            # Фильтрация по цвету
            if selected_color:
                queryset = queryset.filter(color__in=selected_color)

            # Фильтрация по цене
            if min_price is not None:
                queryset = queryset.filter(price__gte=min_price)
            if max_price is not None:
                queryset = queryset.filter(price__lte=max_price)

            # Сортировка по цене
            if direction == 'ascending':
                queryset = queryset.order_by('price')
            elif direction == 'descending':
                queryset = queryset.order_by('-price')
            # Кэшируем результат на 15 минут
            cache.set(cache_key, queryset, 60 * 15)

        return queryset
           
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        categories = set(queryset.values_list('category__name', flat=True))  
        colors = set(queryset.values_list('color', flat=True))# Уникальные категории
        
        # Проверяем, есть ли категории перед их передачей в контекст
        if categories:
            context['categories'] = categories
        else:
            context['categories'] = Product.objects.values_list('category', flat=True).distinct()
        
        if colors:
          context['colors'] = colors
        else:
          context['colors'] = Product.objects.values_list('color', flat=True).distinct()
            
        context['selected_brands'] = self.request.GET.getlist('category')
        context['selected_colors'] = self.request.GET.getlist('color')
        context['max_price'] = self.request.GET.get('max_price')
        context['min_price'] = self.request.GET.get('min_price')
        context['ordering'] = self.request.GET.get('ordering')

        return context
    

class TShirtShopView(ListView):
    context_object_name = 'product_tshirts'
    template_name = 'shop_t-shirt.html'
    model = ProductTshirt
    paginate_by = 9  

    def get_queryset(self):
        selected_brands = self.request.GET.getlist('category')
        selected_color = self.request.GET.getlist('color')
        max_price = self.request.GET.getlist('price')
        min_price = self.request.GET.getlist('-price')

        cache_key = f"tshirt_product:{urlencode(self.request.GET)}"
        queryset = cache.get(cache_key)

        if queryset is None:  # Используем `is None`, чтобы убедиться, что queryset не закэширован
            queryset = ProductTshirt.objects.filter(available=True)
            # Фильтрация по брендам
            if selected_brands:
              queryset = queryset.filter(category__name__in=selected_brands)

            # Фильтрация по цвету
            if selected_color:
              queryset = queryset.filter(color__in=selected_color)

            # Фильтрация по цене  
            if min_price and max_price:
              queryset = queryset.filter(price__gte=min_price, price__lte=max_price)

            direction = self.request.GET.get('direction')
            if direction == 'ascending':
              queryset = queryset.order_by('price')
            if direction == 'descending':
              queryset = queryset.order_by('-price')
            # Кэшируем результат на 15 минут
            cache.set(cache_key, queryset, 60 * 15)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        categories = set(queryset.values_list('category__name', flat=True))  
        colors = set(queryset.values_list('color', flat=True))# Уникальные категории
        
        # Проверяем, есть ли категории перед их передачей в контекст
        if categories:
            context['categories'] = categories
        else:
            context['categories'] = ProductTshirt.objects.values_list('category', flat=True).distinct()
        
        if colors:
          context['colors'] = colors
        else:
          context['colors'] = ProductTshirt.objects.values_list('color', flat=True).distinct()
            
        context['selected_brands'] = self.request.GET.getlist('category')
        context['selected_colors'] = self.request.GET.getlist('color')
        context['max_price'] = self.request.GET.get('max_price')
        context['min_price'] = self.request.GET.get('min_price')
        context['ordering'] = self.request.GET.get('ordering')

        return context
    

class ShortsShopView(ListView):
    context_object_name = 'product_shorts'
    template_name = 'shop_shorts.html'
    model = ProductShorts  
    paginate_by = 9  

    def get_queryset(self):
        selected_brands = self.request.GET.getlist('category')
        selected_color = self.request.GET.getlist('color')
        max_price = self.request.GET.getlist('price')
        min_price = self.request.GET.getlist('-price')

        cache_key = f"shorts_product:{urlencode(self.request.GET)}"
        queryset = cache.get(cache_key)

        if queryset is None:  # Используем `is None`, чтобы убедиться, что queryset не закэширован
            queryset = ProductShorts.objects.filter(available=True)

            if selected_brands:
              queryset = queryset.filter(category__name__in=selected_brands)

            if selected_color:
              queryset = queryset.filter(color__in=selected_color)
              
            if min_price and max_price:
              queryset = queryset.filter(price__gte=min_price, price__lte=max_price)

            direction = self.request.GET.get('direction')
            if direction == 'ascending':
              queryset = queryset.order_by('price')
            if direction == 'descending':
              queryset = queryset.order_by('-price')
            # Кэшируем результат на 15 минут
            cache.set(cache_key, queryset, 60 * 15)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        categories = set(queryset.values_list('category__name', flat=True))  
        colors = set(queryset.values_list('color', flat=True))# Уникальные категории
        
        # Проверяем, есть ли категории перед их передачей в контекст
        if categories:
            context['categories'] = categories
        else:
            context['categories'] = ProductShorts.objects.values_list('category', flat=True).distinct()
        
        if colors:
          context['colors'] = colors
        else:
          context['colors'] = ProductShorts.objects.values_list('color', flat=True).distinct()
            
        context['selected_brands'] = self.request.GET.getlist('category')
        context['selected_colors'] = self.request.GET.getlist('color')
        context['max_price'] = self.request.GET.get('max_price')
        context['min_price'] = self.request.GET.get('min_price')
        context['ordering'] = self.request.GET.get('ordering')

        return context



class SheakersShopView(ListView):
    context_object_name = 'product_sneakers'
    template_name = 'shop_sneakers.html'
    model = ProductSneakers  
    paginate_by = 9  

    def get_queryset(self):
        selected_brands = self.request.GET.getlist('category')
        selected_color = self.request.GET.getlist('color')
        max_price = self.request.GET.getlist('price')
        min_price = self.request.GET.getlist('-price')
        

        cache_key = f"sneakers_product:{urlencode(self.request.GET)}"
        queryset = cache.get(cache_key)

        if queryset is None:  # Используем `is None`, чтобы убедиться, что queryset не закэширован
            queryset = ProductSneakers.objects.filter(available=True)

            if selected_brands:
                queryset = queryset.filter(category__name__in=selected_brands)

            if selected_color:
                queryset = queryset.filter(color__in=selected_color)
              
            if min_price and max_price:
                queryset = queryset.filter(price__gte=min_price, price__lte=max_price)

            direction = self.request.GET.get('direction')
            if direction == 'ascending':
                queryset = queryset.order_by('price')
            if direction == 'descending':
                queryset = queryset.order_by('-price')
            
            # Кэшируем результат на 15 минут
            cache.set(cache_key, queryset, 60 * 15)
           
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        categories = set(queryset.values_list('category__name', flat=True))  
        colors = set(queryset.values_list('color', flat=True))# Уникальные категории
        
        # Проверяем, есть ли категории перед их передачей в контекст
        if categories:
            context['categories'] = categories
        else:
            context['categories'] = ProductSneakers.objects.values_list('category', flat=True).distinct()
        
        if colors:
          context['colors'] = colors
        else:
          context['colors'] = ProductSneakers.objects.values_list('color', flat=True).distinct()
            
        context['selected_brands'] = self.request.GET.getlist('category')
        context['selected_colors'] = self.request.GET.getlist('color')
        context['max_price'] = self.request.GET.get('max_price')
        context['min_price'] = self.request.GET.get('min_price')
        context['ordering'] = self.request.GET.get('ordering')

        return context



def pay_system_view(request):
  cart = Cart(request)
  total_price = cart.get_total_price()
  form = PaySystemForm(initial={'amount': total_price})
  if request.method == 'POST':
    form = PaySystemForm(request.POST)

    if form.is_valid():
      form.clean_cart_number()
      form.clean_data_number()
      form.clean_cvv_number()
      form.clean_amount()

  context = {'form': form}
  return render(request, 'paysystem.html', context)



        
