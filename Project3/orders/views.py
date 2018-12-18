from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.template import loader
from django.core import serializers
from django.forms.models import model_to_dict

from .models import PizzaMenuItem, SubMenuItem, PastaMenuItem, SaladMenuItem, PlatterMenuItem

# Create your views here.

def index(request):
	pizza_list = PizzaMenuItem.objects.order_by('item_name', 'topping_sel', 'price').filter(item_name='Regular'); #order by item name then topping then price
	sicilian_pizza_list = PizzaMenuItem.objects.order_by('item_name', 'topping_sel', 'price').filter(item_name='Sicilian');
	subs_list = SubMenuItem.objects.order_by('item_name', '-size');
	pasta_list = PastaMenuItem.objects.order_by('price');
	salad_list = SaladMenuItem.objects.order_by('price');
	platter_list = PlatterMenuItem.objects.order_by('item_name', '-size');
	template = loader.get_template('orders/index.html')
	context = {
		'pizza_list': pizza_list,
		'sicilian_pizza_list': sicilian_pizza_list,
		'subs_list': subs_list,
		'pasta_list': pasta_list,
		'salad_list': salad_list,
		'platter_list': platter_list,
	}
	return HttpResponse(template.render(context, request))

def item_display(request):
	if request.method == 'POST':
		item_type = request.POST["item_type"];
		item_id = request.POST["item_id"];
		#based on the item's type select the menu with the id and return it as a JSON
		if item_type=='Pizza':
			item = PizzaMenuItem.objects.filter(id=item_id);
	return JsonResponse(item.values()[0]);

def login_view(request):
	if request.method == 'GET':
		return render(request, "orders/login.html")
	elif request.method == 'POST':
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
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
