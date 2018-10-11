from django.db import models

SMALL = 'S'
LARGE = 'L'

SIZE_CHOICES = (
	(SMALL, "Small"),
	(LARGE, "Large"),
)


# Create your models here.
class MenuItem(models.Model):
	#Price
	price = models.DecimalField(max_digits=5, decimal_places=2)

	#Item Type (Pizza/Sub/Pasta/Salad/Platter)
	PIZZA = 'PZA'
	SUB = 'SUB'
	PASTA = 'PTA'
	SALAD = 'SAL'
	PLATTER = 'PLT'

	ITEM_TYPE_CHOICES = (
		(PIZZA, "Pizza"),
		(SUB, "Sub"),
		(PASTA, "Sub"),
		(SALAD, "Salad"),
		(PLATTER, "Platter"),
	)

	item_type = models.CharField(max_length=3, choices = ITEM_TYPE_CHOICES, default = PIZZA);

	item_name = models.CharField(max_length=100);

	#"toString method"
	def __str__(self):
		str(f"{self.item_type} - {self.item_name}");

	class Meta:
		abstract = True

#PizzaMenuItem (inherit MenuItem)
class PizzaMenuItem(MenuItem):
	#Pizza Type (Regular/Sicilian)
	REGULAR = 'RGL'
	SICILIAN = 'SCL'

	PIZZA_TYPE_CHOICES = (
		(REGULAR, "Regular"),
		(SICILIAN, "Sicilian"),
	)

	item_name = models.CharField(max_length=3, choices = PIZZA_TYPE_CHOICES, default = REGULAR)

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
	topping_sel = models.CharField(max_length=1, choices = TOPPING_SEL_CHOICES, default = 'C')

#ToppingMenuItem (though it is technically a menu item, a topping doesn't have an associated price or "type")
class ToppingMenuItem(models.Model):
	#Topping Name
	name = models.CharField(max_length=100);

class SubMenuItem(MenuItem):
	#Sub Size (Small/Large)
	size = models.CharField(max_length=1, choices = SIZE_CHOICES, default = SMALL)

class SaladMenuItem(MenuItem):
	class Meta:
		abstract = False;

class PastaMenuItem(MenuItem):
	class Meta:
		abstract = False;


class PlatterMenuItem(MenuItem):
	#Platter Size (Small/Large)
	size = models.CharField(max_length=1, choices = SIZE_CHOICES, default = SMALL)