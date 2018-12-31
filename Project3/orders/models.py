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
		try:
			return str(f"{self.get_item_type_display()} - {self.item_name} - {self.pizzamenuitem.size} - {self.pizzamenuitem.topping_sel}");
		except PizzaMenuItem.DoesNotExist:
			try:
				return str(f"{self.get_item_type_display()} - {self.item_name} - {self.submenuitem.size}");
			except SubMenuItem.DoesNotExist:
				try:
					return str(f"{self.get_item_type_display()} - {self.item_name} - {self.plattermenuitem.size}");
				except:
					return str(f"{self.get_item_type_display()} - {self.item_name}");

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
		return str(f"{self.item_type} - {self.item_name} - {self.size} - {self.topping_sel}");

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
		return str(f"{self.item_type} - {self.item_name} - {self.size}");
	class Meta:
		verbose_name = "Sub Menu Item"

class SaladMenuItem(MenuItem):
	def __str__(self):
		return str(f"{self.item_type} - {self.item_name}");
	class Meta:
		verbose_name = "Salad Menu Item"

class PastaMenuItem(MenuItem):
	def __str__(self):
		return str(f"{self.item_type} - {self.item_name}");
	class Meta:
		verbose_name = "Pasta Menu Item"


class PlatterMenuItem(MenuItem):

	size = models.CharField(max_length=1, choices = SIZE_CHOICES, default = SMALL)

	class Meta:
		verbose_name = "Platter Menu Item"
	def __str__(self):
		return str(f"{self.item_type} - {self.item_name} - {self.size}");

#Shopping Cart (one shopping cart to many order items)
class ShoppingCart (models.Model):
	#user
	user = models.ForeignKey(User, on_delete=models.CASCADE);

	#compute the total cart price
	total_cost = models.DecimalField(max_digits=5, default = Decimal('0.00'),decimal_places=2,validators=[MinValueValidator(Decimal('0.00'))]);

	ORDER_STATUS_POSS = (
		('0', "In Process"),
		('1', "Order Confirmed"),
	);

	order_status = models.CharField(max_length=1, choices = ORDER_STATUS_POSS, default = '0', verbose_name="Order Status");

	class Meta:
		verbose_name = "Shopping Cart"

	def __str__(self):
		return str(f"{self.user.username}'s Shopping Cart");

#OrderItem
class OrderItem (models.Model):
	#pointer to the item id in the appropriate database based on the item type
	menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE);

	#final price includes the list of price of add ons
	final_price = models.DecimalField(max_digits=5, decimal_places=2,validators=[MinValueValidator(Decimal('0.00'))]);

	add_ons = models.CharField(blank=True, max_length=100); #list of add ons for pizza or subs, separated by commas, can be blank

	#returns the add ons as an array
	def get_add_ons_list(self):
		return self.add_ons.split(',')[0:len(self.add_ons.split(','))-1];

	shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE);
