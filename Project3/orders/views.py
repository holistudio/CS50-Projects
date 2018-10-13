from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

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