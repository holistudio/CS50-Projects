from django.test import TestCase
from django.db.utils import IntegrityError


from .models import PizzaMenuItem

# Create your tests here.
class PizzaMenuItemModelTests(TestCase):

	def test_duplicates(self):
		p1 = PizzaMenuItem(item_name = 'Regular', size = 'L', topping_sel = '1',price = 2.00);
		p1.save()
		p2 = PizzaMenuItem(item_name = 'Regular', size = 'L', topping_sel = '1', price = 1.00)
		with self.assertRaises(Exception) as raised:
			p2.save()
		self.assertEqual(IntegrityError, type(raised.exception))
	
	#negative prices not allowed
	def test_negative_price(self):
		price = -0.01
		p = PizzaMenuItem(price = price);
		self.assertRaises(IntegrityError, p.save());

#blank inputs


#valid character length

#character length exceeded

#normal prices

#price digits exceeded

#invalid choices

#valid choices