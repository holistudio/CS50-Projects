from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.template import loader
from django.core import serializers
from django.forms.models import model_to_dict
from django.utils.timezone import now, localtime
from .models import MenuItem, PizzaMenuItem, SubMenuItem, PastaMenuItem, SaladMenuItem, PlatterMenuItem, ToppingMenuItem, ShoppingCart, OrderItem
from django.core.mail import send_mail

from decimal import *
import math, random, os

#get the current user's shopping cart or create one if it doesn't exist yet.
def get_current_shopping_cart(request):
	if request.user.is_authenticated:
		#get the user shopping cart that's 'in process'
		cart_query = ShoppingCart.objects.filter(user = request.user, order_status='0');
		if len(cart_query)==0:
			#if no shopping cart is found, create one for the user
			new_cart = ShoppingCart(user=request.user);
			new_cart.save();
			return new_cart;
		else:
			#else, get the first in-process cart
			return cart_query.get();
	else:
		#return a string if user is not logged in.
		return 'NO_USER_LOGGED_IN'

# Create your views here.
def index(request):
	#see if user is logged in or not
	if request.user.is_authenticated:
		template = loader.get_template('orders/index.html')
		#load menu items in separate lists
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

		context = {
			'pizza_list': pizza_list,
			'sicilian_pizza_list': sicilian_pizza_list,
			'subs_list': subs_list,
			'pasta_list': pasta_list,
			'salad_list': salad_list,
			'platter_list': platter_list,
			'topping_list':topping_list,
		}

		#load shopping cart into context (esp for displaying shopping cart item count in navbar)
		shopping_cart = get_current_shopping_cart(request);
		if shopping_cart != 'NO_USER_LOGGED_IN':
			context['shopping_cart'] = shopping_cart;
			shopping_cart_items = OrderItem.objects.filter(shopping_cart=shopping_cart);
			context['shopping_cart_items'] = shopping_cart_items;
		return HttpResponse(template.render(context, request))
	else:
		#if user is not logged in, just display the front page, without loading context 
		return render(request, "orders/index.html")

def item_display(request):
	if request.method == 'POST':
		item_type = request.POST["item_type"];
		item_id = request.POST["item_id"];
		itemJSON = {};
		#based on the item's type select the MenuItem with the id and return it as a JSON
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
			itemJSON['error'] = 'Error - Item Not Found';
		itemJSON['item_type'] = item.get_item_type_display();
		itemJSON['item_name'] = item.item_name;
		itemJSON['price'] = item.price;
		return JsonResponse(itemJSON);
	else:
		return HttpResponseRedirect(reverse("orders:index"))

def add_item_to_cart(request):
	if request.method == 'POST':
		#get stuff from form
		menu_item = MenuItem.objects.get(id = request.POST["menu_item_id"]);

		add_ons = '';
		# pizza add ons
		if menu_item.item_type=='PZA':
			num_toppings = int(menu_item.pizzamenuitem.topping_sel);
			if num_toppings>0:
				if num_toppings<4:
					for i in range(0,int(menu_item.pizzamenuitem.topping_sel)):
						key = str(f"topping{i+1}");
						add_ons = str(f"{add_ons},{request.POST[key]}");
				else:
					add_ons = str(f"{add_ons}Sausage,Green Peppers,Onions,Mushrooms");

		#sub add ons
		steak_sub_add_ons = ['extra_mushrooms','extra_green_peppers','extra_onions']
		if menu_item.item_type=='SUB':
			if 'extra_cheese' in request.POST.keys():
				add_ons = str(f"{add_ons},Extra Cheese (+0.50)");

			if menu_item.item_name == 'Steak + Cheese':
				for i in range(0,len(steak_sub_add_ons)):
					if steak_sub_add_ons[i] in request.POST.keys():
						add_ons = str(f"{add_ons},{request.POST[steak_sub_add_ons[i]]} (+0.50)");
		if len(add_ons)>0:
			if add_ons[0]==',':
				add_ons = add_ons[1:];

		#final price from form
		final_price = request.POST['price'];


		#find user's in-process shopping cart
		cart = get_current_shopping_cart(request);
		#create an order item model instance
		o = OrderItem(menu_item=menu_item, final_price = final_price, add_ons = add_ons, shopping_cart = cart);
		o.save();
		cart.save();
	#return to the front page
	return HttpResponseRedirect(reverse("orders:index"))

def shopping_cart(request):
	if request.user.is_authenticated:
		#find the in-process shopping cart for user and display order items
		shopping_cart= get_current_shopping_cart(request);
		shopping_cart_items = OrderItem.objects.filter(shopping_cart=shopping_cart);
		context = {
			'shopping_cart': shopping_cart,
			'shopping_cart_items': shopping_cart_items,
		}
		template = loader.get_template('orders/cart.html')
		return HttpResponse(template.render(context, request));
	else:
		#redirect to front page if user is not logged in
		return HttpResponseRedirect(reverse("orders:index"))


def remove_cart_item(request):
	if request.method == 'POST':
		#get order item id to be deleted
		item_id = request.POST["item_id"];
		o = OrderItem.objects.get(id = item_id);
		#delete item
		o.delete();
		o.shopping_cart.save();
	#return to shopping cart page
	return HttpResponseRedirect(reverse("orders:shopping_cart"))

def check_out(request):
	if request.method == 'POST':
		#find the in-process shopping cart for user and display order items
		shopping_cart= get_current_shopping_cart(request);

		#check if there are items in the shopping cart (total_cost>0)
		if shopping_cart.total_cost>Decimal(0):
			#update shopping cart order status, add confirmation number and time order placed
			shopping_cart.order_status='1';
			shopping_cart.checkout_time = localtime(now());
			conf_num = math.floor(random.random()*1000000);
			shopping_cart.conf_num = conf_num;
			shopping_cart.save();

			#find associated order items, to be displayed in order confirmation email to user
			shopping_cart_items = OrderItem.objects.filter(shopping_cart=shopping_cart);
			context = {
				'shopping_cart': shopping_cart,
				'shopping_cart_items': shopping_cart_items,
				'first_name':request.user.first_name,
			}
			#render html email message
			html_message = loader.render_to_string('orders/order_conf.html',context)

			#email user confirmation email with order confirmation number and items ordered
			send_mail(
			    'Your order for PizzaHub is in the works!',
			    '',
			    os.getenv("SERVER_NO_REPLY_EMAIL"),
			    [shopping_cart.user.email],
			    fail_silently=False,
				html_message=html_message
			);

			#flash success message on front page
			messages.add_message(request, messages.SUCCESS, str(f"Your order is in the works! Order Confirmation #: {conf_num}"))
			return HttpResponseRedirect(reverse("orders:index"));
		else:
			#flash error message if there are no items in cart at checkout
			messages.add_message(request, messages.ERROR, str(f"Please add items before checking out."))
			return HttpResponseRedirect(reverse("orders:shopping_cart"))
	else:
		#flash error message if a non-POST request was made for check out
		messages.add_message(request, messages.ERROR, str(f"Please check out by clicking the checkout button below."))
		return HttpResponseRedirect(reverse("orders:shopping_cart"))

def login_view(request):
	if request.method == 'POST':
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			#find user's in-process shopping cart or create a new one
			get_current_shopping_cart(request);
			return HttpResponseRedirect(reverse("orders:index"))
		else:
			messages.add_message(request, messages.ERROR, str(f"Invalid username or password"))
			return HttpResponseRedirect(reverse("orders:login"))
	else:
		return render(request, "orders/login.html")

def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse("orders:index"))

def register_view(request):
	if request.method =="POST":
		# Get form information.
		username = request.POST["username"]
		password = request.POST["password"]
		confirm = request.POST["pw-conf"]

		first_name = request.POST["first-name"]
		last_name = request.POST["last-name"]
		email = request.POST["email"]

		#make sure password match
		if password != confirm:
			messages.add_message(request, messages.ERROR, str(f"Passwords do not match"))
			return HttpResponseRedirect(reverse("orders:register"))
		#make sure username does not already exist
		try:
			user = User.objects.create_user(username, email, password)
		except IntegrityError as e:
			if(str(e.__cause__)=='UNIQUE constraint failed: auth_user.username'):
				messages.add_message(request, messages.ERROR, str(f"Username already exists"))
				return HttpResponseRedirect(reverse("orders:register"))
			else:
				messages.add_message(request, messages.ERROR, str(f"Invalid inputs"))
				return HttpResponseRedirect(reverse("orders:register"))
		else:
			#set first and last name
			user.first_name = first_name;
			user.last_name = last_name;
			#add username and password to database
			user.save()
			messages.add_message(request, messages.SUCCESS, str(f"You're registered!"))
			return HttpResponseRedirect(reverse("orders:index"))
	else:
		return render(request, "orders/register.html")
