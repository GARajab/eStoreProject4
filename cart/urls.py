from django.urls import path
from . import views
from .views import clear_cart
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.cart_summary, name="cart_summary"),
    path("add/", views.cart_add, name="cart_add"),
    path("delete/", views.cart_delete, name="cart_delete"),
    path("update/", views.cart_update, name="cart_update"),
    path("checkout/", views.checkout, name="checkout"),
    path("payment/<int:order_id>/", views.payment, name="payment"),
    path("clear_cart/", views.clear_cart, name="clear_cart"),
    path("orders/", views.order_list, name="order_list"),
]
