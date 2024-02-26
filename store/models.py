from django.db import models
from django.urls import reverse

from category.models import *
# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.IntegerField()
    images = models.ImageField(upload_to='products/')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    
    def __str__(self) -> str:
        return self.product_name
    
    def get_product_url(self):
        return reverse('store:product_detail', args=[self.category.slug, self.slug])

class VariationManager(models.Manager):
    """This class manager, manages the variation model. It handles database queries instead of doing it manually"""
    
    def colors(self):
        """this calls the constructor of the class 'VariationManager which is the 'models.Manager' to access a method like get() and filter"""
        return super(VariationManager, self).filter(variation_category='color', is_active=True)
    
    def sizes(self):
        """read the first method's docstring"""
        return super(VariationManager, self).filter(variation_category='size', is_active=True)
    


variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)

    
class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)
    
    # This here overrides the default Manager class.
    objects = VariationManager()
    
    def __str__(self) -> str:
        return self.variation_category