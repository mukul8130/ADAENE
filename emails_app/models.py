from django.db import models

# Create your models here.
class email_table(models.Model):
    email=models.EmailField()

