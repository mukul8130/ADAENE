# Generated by Django 4.1.7 on 2024-03-11 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_table',
            name='price',
            field=models.IntegerField(),
        ),
    ]
