from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
	path("", views.index, name="index"),
	path("menuitem/", views.item_display, name="item_display"),
	path("additemtocart/", views.add_item_to_cart, name="add_item_to_cart"),
	path("login/", views.login_view, name="login"),
	path("logout/", views.logout_view, name="logout"),
	path("register/", views.register_view, name="register")
]
