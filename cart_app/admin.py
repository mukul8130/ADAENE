from django.contrib import admin
from .models import Cart_item_table
# Register your models here.

@admin.register(Cart_item_table)
class cde(admin.ModelAdmin):
    list_display=('id','pt','ut','q','is_active')
