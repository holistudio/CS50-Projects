from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import *

#Item Type (Pizza/Sub/Pasta/Salad/Platter)
PIZZA = 'PZA'
SUB = 'SUB'
PASTA = 'PST'
SALAD = 'SAL'
PLATTER = 'PLT'

ITEM_TYPE_CHOICES = (
	(PIZZA, "Pizza"),
	(SUB, "Sub"),
	(PASTA, "Pasta"),
	(SALAD, "Salad"),
	(PLATTER, "Platter"),
)

#Size selections
SMALL = 'S'
LARGE = 'L'

SIZE_CHOICES = (
	(SMALL, "Small"),
	(LARGE, "Large"),
)


# Create your models here.
class MenuItem(models.Model):
	item_type = models.CharField(max_length=3, choices = ITEM_TYPE_CHOICES, default = PIZZA);

	item_name = models.CharField(max_length=100);

	price = models.DecimalField(max_digits=5, decimal_places=2,validators=[MinValueValidator(Decimal('0.00'))])
	def __str__(self):
		def pizzaToString():
			return self.pizzamenuitem.__str__();
		def subToString():
			return self.submenuitem.__str__();
		def platterToString():
			return self.plattermenuitem.__str__();
		def saladToString():
			return self.saladmenuitem.__str__();
		def pastaToString():
			return self.pastamenuitem.__str__();
		def defaultToString():
			return str(f"{self.get_item_type_display()} - {self.item_name} - ${self.price}");
		switcher = {
			PIZZA: pizzaToString,
			SUB: subToString,
			PLATTER: platterToString,
			SALAD: saladToString,
			PASTA: pastaToString,
		}
		return switcher.get(self.item_type, defaultToString)();

	class Meta:
			verbose_name = "Menu Item"
#PizzaMenuItem (inherit MenuItem)
class PizzaMenuItem(MenuItem):
	#Pizza Type (Regular/Sicilian)
	REGULAR = 'Regular'
	SICILIAN = 'Sicilian'

	PIZZA_TYPE_CHOICES = (
		(REGULAR, "Regular"),
		(SICILIAN, "Sicilian"),
	)

	#Topping Selection	(Cheese 0, 1 topping 1, 2 toppings 2, 3 toppings 3, Special 4)
	TOPPING_SEL_CHOICES = (
		('0', "Cheese"),
		('1',"1 topping"),
		('2',"2 toppings"),
		('3',"3 toppings"),
		('4',"Special")
	)

	pizza_type = models.CharField(max_length=100, choices = PIZZA_TYPE_CHOICES, default = REGULAR)

	size = models.CharField(max_length=1, choices = SIZE_CHOICES, default = SMALL)

	topping_sel = models.CharField(max_length=1, choices = TOPPING_SEL_CHOICES, default = '0', verbose_name="Topping Selection")
	#"toString method"
	def __str__(self):
		return str(f"{self.get_item_type_display()} - {self.item_name} - {self.get_size_display()} - {self.pizzamenuitem.get_topping_sel_display()} - ${self.price}");

	class Meta:
			verbose_name = "Pizza Menu Item"

#ToppingMenuItem (though it is technically a menu item, a topping doesn't have an associated price or "type")
class ToppingMenuItem(models.Model):
	#Topping Name
	item_name = models.CharField(max_length=100, unique = True);

	class Meta:
		verbose_name = "Topping Menu Item"

	#"toString method"
	def __str__(self):
		return str(f"TP - {self.item_name}");

class SubMenuItem(MenuItem):

	size = models.CharField(max_length=1, choices = SIZE_CHOICES, default = SMALL)
	def __str__(self):
		return str(f"{self.get_item_type_display()} - {self.item_name} - {self.get_size_display()} - ${self.price}");
	class Meta:
		verbose_name = "Sub Menu Item"

class SaladMenuItem(MenuItem):
	def __str__(self):
		return str(f"{self.get_item_type_display()} - {self.item_name} - ${self.price}");
	class Meta:
		verbose_name = "Salad Menu Item"

class PastaMenuItem(MenuItem):
	def __str__(self):
		return str(f"{self.get_item_type_display()} - {self.item_name} - ${self.price}");
	class Meta:
		verbose_name = "Pasta Menu Item"


class PlatterMenuItem(MenuItem):

	size = models.CharField(max_length=1, choices = SIZE_CHOICES, default = SMALL)

	class Meta:
		verbose_name = "Platter Menu Item"
	def __str__(self):
		return str(f"{self.get_item_type_display()} - {self.item_name} - {self.get_size_display()} - ${self.price}");

#Shopping Cart (one shopping cart to many order items)
class ShoppingCart (models.Model):
	#user
	user = models.ForeignKey(User, on_delete=models.CASCADE);

	#compute the total cart price
	total_cost = models.DecimalField(max_digits=5, default = Decimal('0.00'),decimal_places=2,validators=[MinValueValidator(Decimal('0.00'))]);

	def total_cost_dollars(self):
		return "$ %.2f" % float(self.total_cost) if self.total_cost else 0;
	total_cost_dollars.short_description = "Total Cost"

	ORDER_STATUS_POSS = (
		('0', "In Process"),
		('1', "Order Placed"),
	);

	order_status = models.CharField(max_length=1, choices = ORDER_STATUS_POSS, default = '0', verbose_name="Order Status");

	conf_num = models.IntegerField(blank=True, null=True, verbose_name="Order Confirmation #");
	checkout_time = models.DateTimeField(blank=True, null=True, verbose_name="Time Order Placed");

	class Meta:
		verbose_name = "Shopping Cart"

	def __str__(self):
		return str(f"{self.user.username}'s Shopping Cart");
	def save(self):
		total = Decimal(0);
		shopping_cart_items = OrderItem.objects.filter(shopping_cart=self);
		print(shopping_cart_items);
		for item in shopping_cart_items:
			total = total + item.final_price;
		self.total_cost = Decimal(total);
		super(ShoppingCart, self).save()

#OrderItem
class OrderItem (models.Model):
	#pointer to the item id in the appropriate database based on the item type
	menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE);

	#final price includes the list of price of add ons
	final_price = models.DecimalField(max_digits=5, decimal_places=2,validators=[MinValueValidator(Decimal('0.00'))]);

	def final_price_dollars(self):
		return "$ %.2f" % float(self.final_price) if self.final_price else "$ 0.00";
	final_price_dollars.short_description = "Final Price"
	add_ons = models.CharField(blank=True, max_length=100); #list of add ons for pizza or subs, separated by commas, can be blank

	#returns the add ons as an array
	def get_add_ons_list(self):
		print(self.add_ons.split(','));
		return self.add_ons.split(',');

	shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE);
	def delete(self):
		super(OrderItem, self).delete()
		self.shopping_cart.save();
	def save(self):
		self.final_price = self.menu_item.price;
		if self.menu_item.item_type=='SUB':
			print(self.get_add_ons_list)
			self.final_price = self.final_price + Decimal((len(self.add_ons.split(',')))*0.5);
		super(OrderItem, self).save()
		self.shopping_cart.save();
	def __str__(self):
		return str(f"{self.menu_item.get_item_type_display()} - {self.menu_item.item_name} - ${self.final_price} - {self.shopping_cart}");
