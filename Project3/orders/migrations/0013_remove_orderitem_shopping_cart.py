# Generated by Django 2.1.2 on 2018-12-31 02:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_auto_20181230_2116'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='shopping_cart',
        ),
    ]
