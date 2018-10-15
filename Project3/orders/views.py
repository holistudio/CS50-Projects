from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import IntegrityError

# Create your views here.

def index(request):
	return render(request, "orders/index.html")

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