from django.contrib import admin
from .models import email_table
# Register your models here.
@admin.register(email_table)
class em(admin.ModelAdmin):
    list_display=('id','email')