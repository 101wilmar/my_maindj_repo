from django.contrib.contenttypes.models import ContentType
import unicodedata
from django.db import models
from django.urls import reverse
import uuid
from users.models import User


class Category(models.Model):
  brand = models.CharField(max_length=100)
  name = models.CharField(max_length=100)
  slug = models.SlugField(max_length=100, unique=True)

  class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

  def __str__(self):
        return self.name

  def get_absolute_url(self):
        return reverse('members:product_list_by_category', args=[self.slug])


class Product(models.Model):
  category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
  product_type = models.CharField(max_length=20, null=True, blank=True, unique=True, default=uuid.uuid4)
  name = models.CharField(max_length=150, db_index=True)
  slug = models.CharField(max_length=150, db_index=True, unique=True)
  color = models.CharField(max_length=100)
  price = models.DecimalField(max_digits=5, decimal_places=2)
  picture = models.URLField(blank=False, null=False)
  picture1 = models.URLField(blank=False, null=False)
  picture2 = models.URLField(blank=False, null=False)
  picture3 = models.URLField(blank=False, null=False)
  descript = models.TextField(max_length=400) 
  info = models.TextField(max_length=400) 
  available = models.BooleanField(default=True)
  created = models.DateTimeField(auto_now_add=True)
  uploaded = models.DateTimeField(auto_now=True)

  class Meta:
        ordering = ('name',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        index_together = (('id', 'slug'), )

  def save(self, *args, **kwargs):
    if not self.product_type:
      self.product_type = uuid.uuid4()
    super().save(*args, **kwargs)

  def __str__(self):
        return  self.name

  def get_absolute_url(self):
        return reverse('members:product_detail', args=[self.id, self.slug])
  

class ProductTshirt(models.Model):
  category = models.ForeignKey(Category,
                                 related_name='product_tshirts',
                                 on_delete=models.CASCADE)
  product_type = models.CharField(max_length=20, null=True, blank=True, unique=True, default=uuid.uuid4)
  name = models.CharField(max_length=150, db_index=True)
  slug = models.CharField(max_length=150, db_index=True, unique=True)
  color = models.CharField(max_length=100)
  price = models.DecimalField(max_digits=5, decimal_places=2)
  picture = models.URLField(blank=False, null=False)
  picture1 = models.URLField(blank=False, null=False)
  picture2 = models.URLField(blank=False, null=False)
  picture3 = models.URLField(blank=False, null=False)
  descript = models.TextField(max_length=400) 
  info = models.TextField(max_length=400) 
  available = models.BooleanField(default=True)
  created = models.DateTimeField(auto_now_add=True)
  uploaded = models.DateTimeField(auto_now=True)

  class Meta:
        ordering = ('name',)
        verbose_name = 'Товар Футболка'
        verbose_name_plural = 'Товары Футболки'
        index_together = (('id', 'slug'), )

  def save(self, *args, **kwargs):
    if not self.product_type:
      self.product_type = uuid.uuid4()
    super().save(*args, **kwargs)

  def __str__(self):
        return  self.name

  def get_absolute_url(self):
        return reverse('members:product_detail_tshirt', args=[self.id, self.slug])
  

class ProductShorts(models.Model):
  category = models.ForeignKey(Category,
                                 related_name='product_shorts',
                                 on_delete=models.CASCADE)
  product_type = models.CharField(max_length=20, null=True, blank=True, unique=True, default=uuid.uuid4)
  name = models.CharField(max_length=150, db_index=True)
  slug = models.CharField(max_length=150, db_index=True, unique=True)
  color = models.CharField(max_length=100)
  price = models.DecimalField(max_digits=5, decimal_places=2)
  picture = models.URLField(blank=False, null=False)
  picture1 = models.URLField(blank=False, null=False)
  picture2 = models.URLField(blank=False, null=False)
  picture3 = models.URLField(blank=False, null=False)
  descript = models.TextField(max_length=400) 
  info = models.TextField(max_length=400) 
  available = models.BooleanField(default=True)
  created = models.DateTimeField(auto_now_add=True)
  uploaded = models.DateTimeField(auto_now=True)

  class Meta:
        ordering = ('name',)
        verbose_name = 'Товар Шорты'
        verbose_name_plural = 'Товары Шорты'
        index_together = (('id', 'slug'), )

  def save(self, *args, **kwargs):
    if not self.product_type:
      self.product_type = uuid.uuid4()
    super().save(*args, **kwargs)

  def __str__(self):
        return  self.name

  def get_absolute_url(self):
        return reverse('members:product_detail_shorts', args=[self.id, self.slug])
  

class ProductSneakers(models.Model):
  category = models.ForeignKey(Category,
                                 related_name='product_sneakers',
                                 on_delete=models.CASCADE)
  product_type = models.CharField(max_length=20, null=True, blank=True, unique=True, default=uuid.uuid4)
  name = models.CharField(max_length=150, db_index=True)
  slug = models.CharField(max_length=150, db_index=True, unique=True)
  color = models.CharField(max_length=100)
  price = models.DecimalField(max_digits=5, decimal_places=2)
  picture = models.URLField(blank=False, null=False)
  picture1 = models.URLField(blank=False, null=False)
  picture2 = models.URLField(blank=False, null=False)
  picture3 = models.URLField(blank=False, null=False)
  descript = models.TextField(max_length=400) 
  info = models.TextField(max_length=400) 
  available = models.BooleanField(default=True)
  created = models.DateTimeField(auto_now_add=True)
  uploaded = models.DateTimeField(auto_now=True)

  class Meta:
        ordering = ('name',)
        verbose_name = 'Товар Кроссовки'
        verbose_name_plural = 'Товары Кроссовки'
        index_together = (('id', 'slug'), )

  def save(self, *args, **kwargs):
    if not self.product_type:
      self.product_type = uuid.uuid4()
    super().save(*args, **kwargs)

  def __str__(self):
        return  self.name

  def get_absolute_url(self):
        return reverse('members:product_detail_sneakers', args=[self.id, self.slug])
  

class Action(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product_id = models.IntegerField()
    product_type = models.CharField(max_length=80)
    action_type = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)