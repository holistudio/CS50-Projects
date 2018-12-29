import csv

from orders.models import PizzaMenuItem, SubMenuItem, PastaMenuItem, SaladMenuItem, PlatterMenuItem, ToppingMenuItem


f = open("menu.csv")
reader = csv.reader(f)

for itemType,itemName,itemSize,price,toppingSel in reader:
	if itemType == 'PZA':
		q = PizzaMenuItem(item_type=itemType, item_name = itemName, pizza_type = itemName, size = itemSize[0], price = price, topping_sel=toppingSel[0])
	if itemType == 'SUB':
		q = SubMenuItem(item_type=itemType, item_name = itemName, size = itemSize[0], price = price)
	if itemType =='PLT':
		q = PlatterMenuItem(item_type=itemType, item_name = itemName, size = itemSize[0], price = price)
	if itemType =='SAL':
		q = SaladMenuItem(item_type=itemType, item_name = itemName, price = price)
	if itemType =='PST':
		q = PastaMenuItem(item_type=itemType, item_name = itemName, price = price)
	if itemType =='TP':
		q = ToppingMenuItem(item_name = itemName)
	q.save();
