from django.contrib import admin
from .models import Category_table
# Register your models here.
@admin.register(Category_table)
class Xyz(admin.ModelAdmin):
    list_display=('id','category_name','slug','created_date','modified_date')
    prepopulated_fields={'slug':('category_name',)}