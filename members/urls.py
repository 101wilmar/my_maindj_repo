from django.urls import include, path
from . import views
from .views import SheakersShopView, ShopListView, ShortsShopView, TShirtShopView
from django.views.decorators.cache import cache_page


app_name = 'members'

urlpatterns = [
      path('members/' , cache_page(60)(views.members), name='members'), 
     
      path('pay/', views.pay_system_view, name='pay'),

      path('shop/', cache_page(10)(ShopListView.as_view()) , name='shop'),
      path('shop/<int:id>/<slug:slug>', views.product_detail_product,
         name='product_detail'),

      path('shop-tshirt/', cache_page(10)(TShirtShopView.as_view()), name='shop_tshirt'),
      path('shop-tshirt/<int:id>/<slug:slug>/', views.product_detail_product_tshirt,
           name='product_detail_tshirt'),

      path('shop-shorts/', cache_page(10)(ShortsShopView.as_view()), name='shop_shorts'),
      path('shop-shorts/<int:id>/<slug:slug>/', views.product_detail_shorts,
           name='product_detail_shorts'),

      path('shop-sneakers/', cache_page(10)(SheakersShopView.as_view()), name='shop_sneakers'),
      path('shop-sneakers/<int:id>/<slug:slug>/', views.product_detail_sneakers,
           name='product_detail_sneakers'),
]
