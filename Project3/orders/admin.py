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
	list_display=['item_name']
	fields = ['item_name']
	ordering = ['id']

class SizeMenuItemAdmin(admin.ModelAdmin):
	#for items with size
	list_display = ('item_type','item_name', 'size', 'price')
	fields = ['item_type','item_name', 'size', 'price']

class PizzaMenuItemAdmin(admin.ModelAdmin):
	#for pizzas
	list_display = ('item_type','item_name', 'pizza_type','size', 'topping_sel', 'price')
	fields = ['item_type','item_name', 'pizza_type','size', 'topping_sel', 'price']

class OrderItemInline(admin.StackedInline):
	model = OrderItem
	extra = 0;
	fields = ['menu_item', 'add_ons','final_price_dollars',];
	readonly_fields = ['final_price_dollars',];

class ShoppingCartAdmin(admin.ModelAdmin):
	list_display = ('user','total_cost', 'order_status','checkout_time','conf_num');
	list_filter = ('order_status',);
	ordering = ['-order_status','checkout_time']
	fields = ['user', 'order_status','checkout_time','conf_num','total_cost_dollars',];
	readonly_fields = ['total_cost_dollars',];
	#display all order items
	inlines = [OrderItemInline]

admin.site.register(MenuItem, GenMenuItemAdmin)
admin.site.register(PizzaMenuItem, PizzaMenuItemAdmin)
admin.site.register(SubMenuItem, SizeMenuItemAdmin)
admin.site.register(PastaMenuItem, SimpleMenuItemAdmin)
admin.site.register(SaladMenuItem, SimpleMenuItemAdmin)
admin.site.register(PlatterMenuItem, SizeMenuItemAdmin)
admin.site.register(ToppingMenuItem, ToppingMenuItemAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
