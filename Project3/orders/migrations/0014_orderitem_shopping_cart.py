# Generated by Django 2.1.2 on 2018-12-31 02:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0013_remove_orderitem_shopping_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='shopping_cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.ShoppingCart'),
            preserve_default=False,
        ),
    ]
