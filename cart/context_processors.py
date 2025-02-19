from .cart import Cart
from django.contrib.auth import get_user_model

User = get_user_model()


def get_user_count(request):
    num_users = User.objects.count()
    return {"num_users": num_users}


def cart(request):
    return {"cart": Cart(request)}
