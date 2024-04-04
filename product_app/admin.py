from django.contrib import admin
from .models import Product_table,Variation_table
# Register your models here.
@admin.register(Product_table)
class bcd(admin.ModelAdmin):
    list_display=('id','product_name','slug','price','stock','discription','image','is_available','category','created_date','modified_date')

    prepopulated_fields={'slug':('product_name',)}


@admin.register(Variation_table)

class yzx(admin.ModelAdmin):
    list_display=('id','variation_category','variation_value','pt')
