from django.db import models
from category_app .models import Category_table
# Create your models here.
class Product_table(models.Model):
    product_name=models.CharField(max_length=100)
    slug=models.SlugField(max_length=100)
    price=models.IntegerField()
    stock=models.IntegerField()
    discription=models.TextField(max_length=500,blank=True)
    image=models.ImageField(upload_to='pro_img')
    is_available=models.BooleanField(default=True)
    category=models.ForeignKey(Category_table,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name
    
class Variation_table(models.Model):
    pt=models.ForeignKey(Product_table,on_delete=models.CASCADE)
    variation_category=models.CharField(max_length=100,choices=[('color','color'),('size','size')])
    variation_value=models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now=True)