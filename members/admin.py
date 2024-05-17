
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Product, ProductShorts, ProductSneakers, ProductTshirt

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'image_show', 'price', 'available', 'created', 'uploaded']
    list_filter = ['available', 'created', 'uploaded']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name', )}


    def image_show(self, obj):
      if obj.picture:
        if hasattr(obj.picture, 'url'):
            return mark_safe("<img src='{}' width='60' />".format(obj.picture.url))
        return mark_safe("<img src='{}' width='60' />".format(obj.picture))
      return "None"

    image_show.__name__ = "Картинка"


@admin.register(ProductTshirt)
class ProductTshirtAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'image_show', 'price', 'available', 'created', 'uploaded']
    list_filter = ['available', 'created', 'uploaded']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name', )}


    def image_show(self, obj):
      if obj.picture:
        if hasattr(obj.picture, 'url'):
            return mark_safe("<img src='{}' width='60' />".format(obj.picture.url))
        return mark_safe("<img src='{}' width='60' />".format(obj.picture))
      return "None"

    image_show.__name__ = "Картинка"


@admin.register(ProductShorts)
class ProductShortsAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'image_show', 'price', 'available', 'created', 'uploaded']
    list_filter = ['available', 'created', 'uploaded']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name', )}


    def image_show(self, obj):
      if obj.picture:
        if hasattr(obj.picture, 'url'):
            return mark_safe("<img src='{}' width='60' />".format(obj.picture.url))
        return mark_safe("<img src='{}' width='60' />".format(obj.picture))
      return "None"

    image_show.__name__ = "Картинка"


@admin.register(ProductSneakers)
class ProductSneakerssAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'image_show', 'price', 'available', 'created', 'uploaded']
    list_filter = ['available', 'created', 'uploaded']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name', )}


    def image_show(self, obj):
      if obj.picture:
        if hasattr(obj.picture, 'url'):
            return mark_safe("<img src='{}' width='60' />".format(obj.picture.url))
        return mark_safe("<img src='{}' width='60' />".format(obj.picture))
      return "None"

    image_show.__name__ = "Картинка"

