from django.contrib import admin

# Register your models here.
from .models import MenuItem, PizzaMenuItem, SubMenuItem, PastaMenuItem, SaladMenuItem, PlatterMenuItem, ToppingMenuItem, OrderItem, ShoppingCart

class GenMenuItemAdmin(admin.ModelAdmin):
	list_display = ('item_type', 'item_name', 'price')
	fields = ['item_type', 'item_name', 'price']

class SimpleMenuItemAdmin(admin.ModelAdmin):
	list_display = ('item_type','item_name', 'price')
	fields = ['item_type','item_name', 'price']

class ToppingMenuItemAdmin(admin.ModelAdmin):
	fields = ['item_name']

class SizeMenuItemAdmin(admin.ModelAdmin):
	#for items with size
	list_display = ('item_type','item_name', 'size', 'price')
	fields = ['item_type','item_name', 'size', 'price']

class PizzaMenuItemAdmin(admin.ModelAdmin):
	#for pizzas
	list_display = ('item_type','item_name', 'pizza_type','size', 'topping_sel', 'price')
	fields = ['item_type','item_name', 'pizza_type','size', 'topping_sel', 'price']

class OrderItemAdmin(admin.ModelAdmin):
	list_display = ('menu_item', 'add_ons', 'final_price')
	fields = ['menu_item', 'add_ons', 'final_price']

class ShoppingCartAdmin(admin.ModelAdmin):
	list_display = ('user','total_cost');
	fields = ['user','total_cost'];

admin.site.register(MenuItem, GenMenuItemAdmin)
admin.site.register(PizzaMenuItem, PizzaMenuItemAdmin)
admin.site.register(SubMenuItem, SizeMenuItemAdmin)
admin.site.register(PastaMenuItem, SimpleMenuItemAdmin)
admin.site.register(SaladMenuItem, SimpleMenuItemAdmin)
admin.site.register(PlatterMenuItem, SizeMenuItemAdmin)
admin.site.register(ToppingMenuItem, ToppingMenuItemAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
