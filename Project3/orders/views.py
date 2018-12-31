from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.template import loader
from django.core import serializers
from django.forms.models import model_to_dict

from .models import MenuItem, PizzaMenuItem, SubMenuItem, PastaMenuItem, SaladMenuItem, PlatterMenuItem, ToppingMenuItem, ShoppingCart, OrderItem

from decimal import *
# Create your views here.

def index(request):
	pizza_list = PizzaMenuItem.objects.order_by('item_name', 'topping_sel', 'price').filter(item_name='Regular'); #order by item name then topping then price
	sicilian_pizza_list = PizzaMenuItem.objects.order_by('item_name', 'topping_sel', 'price').filter(item_name='Sicilian');
	subs_list = SubMenuItem.objects.order_by('item_name', '-size');
	pasta_list = PastaMenuItem.objects.order_by('price');
	salad_list = SaladMenuItem.objects.order_by('price');
	platter_list = PlatterMenuItem.objects.order_by('item_name', '-size');
	topping_queryDict = list(ToppingMenuItem.objects.values('item_name'));
	topping_list = [];
	for item in topping_queryDict:
		topping_list.append(item['item_name']);
	template = loader.get_template('orders/index.html')
	context = {
		'pizza_list': pizza_list,
		'sicilian_pizza_list': sicilian_pizza_list,
		'subs_list': subs_list,
		'pasta_list': pasta_list,
		'salad_list': salad_list,
		'platter_list': platter_list,
		'topping_list':topping_list,
	}
	return HttpResponse(template.render(context, request))

def item_display(request):
	if request.method == 'POST':
		item_type = request.POST["item_type"];
		item_id = request.POST["item_id"];
		itemJSON = {};
		#based on the item's type select the menu with the id and return it as a JSON
		if item_type=='Pizza':
			item = PizzaMenuItem.objects.get(id=item_id);
			itemJSON={'size' : item.get_size_display(),
				'topping_sel': item.topping_sel,
				'topping_sel_display': item.get_topping_sel_display(),
				};
		elif item_type == 'Sub':
			item = SubMenuItem.objects.get(id=item_id);
			itemJSON={'size' : item.get_size_display()}
		elif item_type=='Pasta':
			item = PastaMenuItem.objects.get(id=item_id);
		elif item_type=='Salad':
			item = SaladMenuItem.objects.get(id=item_id);
		elif item_type=='Platter':
			item = PlatterMenuItem.objects.get(id=item_id);
			itemJSON={'size' : item.get_size_display()};
		else:
			#error
			print('Error: item type not recognized');
		itemJSON['item_type'] = item.get_item_type_display();
		itemJSON['item_name'] = item.item_name;
		itemJSON['price'] = item.price;
	return JsonResponse(itemJSON);

def add_item_to_cart(request):
	if request.method == 'POST':


		#get stuff from form
		menu_item = MenuItem.objects.get(id = request.POST["menu_item_id"]);
		# print(menu_item.pizzamenuitem.topping_sel);

		add_ons = '';
		# pizza add ons
		if menu_item.item_type=='PZA':
			num_toppings = int(menu_item.pizzamenuitem.topping_sel);
			if num_toppings>0:
				if num_toppings<4:
					for i in range(0,int(menu_item.pizzamenuitem.topping_sel)):
						key = str(f"topping{i+1}");
						add_ons = str(f"{add_ons}{request.POST[key]}, ");
				else:
					add_ons = str(f"{add_ons}Sausage, Green Peppers, Onions, Mushrooms, ");

		#sub add ons
		steak_sub_add_ons = ['extra_mushrooms','extra_green_peppers','extra_onions']
		if menu_item.item_type=='SUB':
			if 'extra_cheese' in request.POST.keys():
				add_ons = str(f"{add_ons}Extra Cheese, ");

			if menu_item.item_name == 'Steak + Cheese':
				for i in range(0,len(steak_sub_add_ons)):
					if steak_sub_add_ons[i] in request.POST.keys():
						add_ons = str(f"{add_ons}{request.POST[steak_sub_add_ons[i]]}, ");

		#final price from form
		final_price = request.POST['price'];

		#create an order item model instance
		if request.user.is_authenticated:

			cart_query = ShoppingCart.objects.filter(user = request.user);

			if len(cart_query)>0:
				cart=cart_query[0];
			else:
				new_cart = ShoppingCart(user=request.user);
				new_cart.save();
				cart = new_cart;
			o = OrderItem(menu_item=menu_item, final_price = final_price, add_ons = add_ons, shopping_cart = cart);
			o.save();
			cart.total_cost = cart.total_cost + Decimal(final_price);
			cart.save();
		#if there isn't a shopping cart, create an instance

	return HttpResponseRedirect(reverse("orders:index"))

def shopping_cart(request):
	shopping_cart= ShoppingCart.objects.get(user = request.user);
	shopping_cart_items = OrderItem.objects.filter(shopping_cart=shopping_cart);
	context = {
		'shopping_cart': shopping_cart,
		'shopping_cart_items': shopping_cart_items,
	}
	template = loader.get_template('orders/cart.html')
	return HttpResponse(template.render(context, request));

def check_out(request):
	shopping_cart= ShoppingCart.objects.get(user = request.user);
	shopping_cart.order_status='1';
	shopping_cart.save();
	return HttpResponseRedirect(reverse("orders:index"));

def login_view(request):
	if request.method == 'GET':
		return render(request, "orders/login.html")
	elif request.method == 'POST':
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			#create a unique shopping cart model instance
			cart = ShoppingCart(user = user);
			cart.save();
			return HttpResponseRedirect(reverse("orders:index"))
		else:
			return render(request, "orders/login.html", {"message": "Invalid username or password"})

def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse("orders:index"))

def register_view(request):
	if request.method =="POST":

		# Get form information.
		username = request.POST["username"]
		email = request.POST["email"]
		password = request.POST["password"]
		confirm = request.POST["pw-conf"]

		#make sure password match
		if password != confirm:
			return render(request, "orders/register.html", {"message": "Passwords do not match"})
		#make sure username does not already exist
		try:
			user = User.objects.create_user(username, email, password)
		except IntegrityError as e:
			if(str(e.__cause__)=='UNIQUE constraint failed: auth_user.username'):
				return render(request, "orders/register.html", {"message": "Username already exists"})
			else:
				return render(request, "orders/register.html", {"message": "Invalid inputs"})
		else:
			#add username and password to database
			user.save()
			return HttpResponseRedirect(reverse("orders:index"))
	else:
		return render(request, "orders/register.html")
