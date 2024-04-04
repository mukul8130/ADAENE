# Generated by Django 4.1.7 on 2024-03-26 11:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product_app', '0004_variation_table'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart_item_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('q', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('pt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_app.product_table')),
                ('ut', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vt', models.ManyToManyField(to='product_app.variation_table')),
            ],
        ),
    ]