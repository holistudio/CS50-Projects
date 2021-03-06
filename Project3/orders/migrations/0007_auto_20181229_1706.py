# Generated by Django 2.1.2 on 2018-12-29 22:06

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20181208_1654'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_type', models.CharField(choices=[('PZA', 'Pizza'), ('SUB', 'Sub'), ('PST', 'Pasta'), ('SAL', 'Salad'), ('PLT', 'Platter')], default='PZA', max_length=3)),
                ('item_name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
            ],
        ),
        migrations.AlterModelOptions(
            name='shoppingcart',
            options={'verbose_name': 'Shopping Cart'},
        ),
        migrations.AddField(
            model_name='pizzamenuitem',
            name='pizza_type',
            field=models.CharField(choices=[('Regular', 'Regular'), ('Sicilian', 'Sicilian')], default='Regular', max_length=100),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='total_cost',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
        migrations.AlterUniqueTogether(
            name='pastamenuitem',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='pizzamenuitem',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='plattermenuitem',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='saladmenuitem',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='submenuitem',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='pastamenuitem',
            name='id',
        ),
        migrations.RemoveField(
            model_name='pastamenuitem',
            name='item_name',
        ),
        migrations.RemoveField(
            model_name='pastamenuitem',
            name='item_type',
        ),
        migrations.RemoveField(
            model_name='pastamenuitem',
            name='price',
        ),
        migrations.RemoveField(
            model_name='pizzamenuitem',
            name='id',
        ),
        migrations.RemoveField(
            model_name='pizzamenuitem',
            name='item_name',
        ),
        migrations.RemoveField(
            model_name='pizzamenuitem',
            name='item_type',
        ),
        migrations.RemoveField(
            model_name='pizzamenuitem',
            name='price',
        ),
        migrations.RemoveField(
            model_name='plattermenuitem',
            name='id',
        ),
        migrations.RemoveField(
            model_name='plattermenuitem',
            name='item_name',
        ),
        migrations.RemoveField(
            model_name='plattermenuitem',
            name='item_type',
        ),
        migrations.RemoveField(
            model_name='plattermenuitem',
            name='price',
        ),
        migrations.RemoveField(
            model_name='saladmenuitem',
            name='id',
        ),
        migrations.RemoveField(
            model_name='saladmenuitem',
            name='item_name',
        ),
        migrations.RemoveField(
            model_name='saladmenuitem',
            name='item_type',
        ),
        migrations.RemoveField(
            model_name='saladmenuitem',
            name='price',
        ),
        migrations.RemoveField(
            model_name='submenuitem',
            name='id',
        ),
        migrations.RemoveField(
            model_name='submenuitem',
            name='item_name',
        ),
        migrations.RemoveField(
            model_name='submenuitem',
            name='item_type',
        ),
        migrations.RemoveField(
            model_name='submenuitem',
            name='price',
        ),
        migrations.AddField(
            model_name='pastamenuitem',
            name='menuitem_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='orders.MenuItem'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pizzamenuitem',
            name='menuitem_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='orders.MenuItem'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='plattermenuitem',
            name='menuitem_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='orders.MenuItem'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='saladmenuitem',
            name='menuitem_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='orders.MenuItem'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='submenuitem',
            name='menuitem_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='orders.MenuItem'),
            preserve_default=False,
        ),
    ]
