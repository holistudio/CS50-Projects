from django.db import models
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

	#"toString method"
	def __str__(self):
		return str(f"{self.item_type} - {self.item_name}");

	class Meta:
		abstract = True

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
	item_type = models.CharField(max_length=3, choices = ITEM_TYPE_CHOICES, default = PIZZA);

	item_name = models.CharField(max_length=100, choices = PIZZA_TYPE_CHOICES, default = REGULAR)

	size = models.CharField(max_length=1, choices = SIZE_CHOICES, default = SMALL)

	topping_sel = models.CharField(max_length=1, choices = TOPPING_SEL_CHOICES, default = '0', verbose_name="Topping Selection")

	class Meta:
			verbose_name = "Pizza Menu Item"
			unique_together = ('item_type','item_name','size','topping_sel')

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
	item_type = models.CharField(max_length=3, choices = ITEM_TYPE_CHOICES, default = SUB);

	size = models.CharField(max_length=1, choices = SIZE_CHOICES, default = SMALL)

	class Meta:
		verbose_name = "Sub Menu Item"
		unique_together = ('item_type','item_name','size')

class SaladMenuItem(MenuItem):
	item_type = models.CharField(max_length=3, choices = ITEM_TYPE_CHOICES, default = SALAD);
	class Meta:
		verbose_name = "Salad Menu Item"
		unique_together = ('item_type','item_name')

class PastaMenuItem(MenuItem):
	item_type = models.CharField(max_length=3, choices = ITEM_TYPE_CHOICES, default = PASTA);
	class Meta:
		verbose_name = "Pasta Menu Item"
		unique_together = ('item_type','item_name')


class PlatterMenuItem(MenuItem):
	item_type = models.CharField(max_length=3, choices = ITEM_TYPE_CHOICES, default = PLATTER);

	size = models.CharField(max_length=1, choices = SIZE_CHOICES, default = SMALL)

	class Meta:
		verbose_name = "Platter Menu Item"
		unique_together = ('item_type','item_name','size')

#OrderItem
#shows the base price
#If it's a pizza with more than zero toppings and not special pizza display the corresponding number of rows for topping dropdown menu
#If it's a sub, provide add cheese options
#If it's a steak and cheese sub show check boxes for optional toppings
#compute the total price based on the add-on's
#Form will be displayed no matter what to confirm with the user before adding to the shopping cart.

#Shopping Cart (one shopping cart to manny order items)
#items with total prices
#compute the total cart price