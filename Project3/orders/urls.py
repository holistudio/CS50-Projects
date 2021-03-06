from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
	path("", views.index, name="index"),
	path("menuitem/", views.item_display, name="item_display"),
	path("additemtocart/", views.add_item_to_cart, name="add_item_to_cart"),
	path("shoppingcart/", views.shopping_cart, name="shopping_cart"),
	path("removecartitem/", views.remove_cart_item, name="remove_cart_item"),
	path("checkout/", views.check_out, name="check_out"),
	path("login/", views.login_view, name="login"),
	path("logout/", views.logout_view, name="logout"),
	path("register/", views.register_view, name="register")
]
