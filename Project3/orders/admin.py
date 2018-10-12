from django.contrib import admin

# Register your models here.
from .models import PizzaMenuItem, SubMenuItem, PastaMenuItem, SaladMenuItem, PlatterMenuItem

class SimpleMenuItemAdmin(admin.ModelAdmin):
	list_display = ('item_name', 'price')
	fields = ['item_name', 'price']

class SizeMenuItemAdmin(admin.ModelAdmin):
	#for items with size
	list_display = ('item_name', 'size', 'price')
	fields = ['item_name', 'size', 'price']

class PizzaMenuItemAdmin(admin.ModelAdmin):
	#for pizzas
	list_display = ('item_name', 'size', 'topping_sel', 'price')
	fields = ['item_name', 'size', 'topping_sel', 'price']




admin.site.register(PizzaMenuItem, PizzaMenuItemAdmin)
admin.site.register(SubMenuItem, SizeMenuItemAdmin)
admin.site.register(PastaMenuItem, SimpleMenuItemAdmin)
admin.site.register(SaladMenuItem, SimpleMenuItemAdmin)
admin.site.register(PlatterMenuItem, SizeMenuItemAdmin)