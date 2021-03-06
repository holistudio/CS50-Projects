# Generated by Django 2.1.2 on 2018-12-08 21:54

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('orders', '0005_auto_20181115_1304'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('final_price', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('add_ons', models.CharField(max_length=100)),
                ('comments', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
            ],
        ),
        migrations.AlterField(
            model_name='pizzamenuitem',
            name='topping_sel',
            field=models.CharField(choices=[('0', 'Cheese'), ('1', '1 topping'), ('2', '2 toppings'), ('3', '3 toppings'), ('4', 'Special')], default='0', max_length=1, verbose_name='Topping Selection'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='shopping_cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.ShoppingCart'),
        ),
    ]
