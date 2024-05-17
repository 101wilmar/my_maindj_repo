from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<str:product_type>/', views.cart_add, name='cart_add'),
    path('cart/remove/<str:product_type>/', views.cart_remove, name='cart_remove'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
]