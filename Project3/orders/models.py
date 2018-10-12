from django.db import models

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

	#Price
	price = models.DecimalField(max_digits=5, decimal_places=2)

	#"toString method"
	def __str__(self):
		return str(f"{self.item_type} - {self.item_name}");

	class Meta:
		abstract = True

#PizzaMenuItem (inherit MenuItem)
class PizzaMenuItem(MenuItem):
	class Meta:
		verbose_name = "Pizza Menu Item"

	item_type = models.CharField(max_length=3, choices = ITEM_TYPE_CHOICES, default = PIZZA);

	#Pizza Type (Regular/Sicilian)
	REGULAR = 'Regular'
	SICILIAN = 'Sicilian'

	PIZZA_TYPE_CHOICES = (
		(REGULAR, "Regular"),
		(SICILIAN, "Sicilian"),
	)

	item_name = models.CharField(max_length=100, choices = PIZZA_TYPE_CHOICES, default = REGULAR)

	#Pizza Size (Small/Large)
	size = models.CharField(max_length=1, choices = SIZE_CHOICES, default = SMALL)

	#Topping Selection	(Cheese 0, 1 topping 1, 2 toppings 2, 3 toppings 3, Special 4)
	TOPPING_SEL_CHOICES = (
		('C', "Cheese"),
		('1',"1 topping"),
		('2',"2 toppings"),
		('3',"3 toppings"),
		('S',"Special")
	)
	topping_sel = models.CharField(max_length=1, choices = TOPPING_SEL_CHOICES, default = 'C', verbose_name="Topping Selection")

#ToppingMenuItem (though it is technically a menu item, a topping doesn't have an associated price or "type")
class ToppingMenuItem(models.Model):
	class Meta:
		verbose_name = "Topping Menu Item"

	#Topping Name
	item_name = models.CharField(max_length=100);

	#"toString method"
	def __str__(self):
		return str(f"TP - {self.item_name}");

class SubMenuItem(MenuItem):
	class Meta:
		verbose_name = "Sub Menu Item"

	item_type = models.CharField(max_length=3, choices = ITEM_TYPE_CHOICES, default = SUB);
	#Sub Size (Small/Large)
	size = models.CharField(max_length=1, choices = SIZE_CHOICES, default = SMALL)

class SaladMenuItem(MenuItem):
	class Meta:
		verbose_name = "Salad Menu Item"
	item_type = models.CharField(max_length=3, choices = ITEM_TYPE_CHOICES, default = SALAD);

class PastaMenuItem(MenuItem):
	class Meta:
		verbose_name = "Pasta Menu Item"
	item_type = models.CharField(max_length=3, choices = ITEM_TYPE_CHOICES, default = PASTA);


class PlatterMenuItem(MenuItem):
	class Meta:
		verbose_name = "Platter Menu Item"
	item_type = models.CharField(max_length=3, choices = ITEM_TYPE_CHOICES, default = PLATTER);
	#Platter Size (Small/Large)
	size = models.CharField(max_length=1, choices = SIZE_CHOICES, default = SMALL)