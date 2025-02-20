from django.shortcuts import get_object_or_404, render, redirect
from .models import Category, Product
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms
import random
from cart.models import Order
from django.db.models import Sum
from django.http import HttpResponse


def home(request):
    products = Product.objects.all()
    return render(request, "home.html", {"products": products})


def about(request):
    return render(request, "about.html", {})


def AdminPanel(request):
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(total=Sum("total_price"))["total"] or 0
    num_users = User.objects.count()

    context = {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "total_users": num_users,
    }
    return render(request, "adminPanel/index.html", context)


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Welcome Back " + username))
            return redirect("home")
        else:
            messages.warning(request, ("There Was An Error Try Again Later"))
            return redirect("login")

    else:
        return render(request, "login.html", {})


def logout_user(request):
    logout(request)
    messages.info(request, ("You Are LogedOut Successfully!"))
    return redirect("home")


def category(request, rjb):
    rjb = rjb.replace("-", "")
    try:
        category = Category.objects.get(name=rjb)
        products = Product.objects.filter(category=category)

        # Check if there are no products in the category
        if not products.exists():
            messages.info(
                request,
                f"There are no products available in the category '{category.name}'.",
            )
            return redirect("home")

        return render(
            request, "category.html", {"products": products, "category": category}
        )

    except Category.DoesNotExist:
        messages.warning(request, ("This Category Is Not Available"))
        return redirect("home")


def product(request, pk):

    product = get_object_or_404(Product, id=pk)

    return render(request, "product.html", {"product": product})


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST["firstName"]
        last_name = request.POST["lastName"]
        email = request.POST["email"]
        password = request.POST["password"]

        # Validate the data (you can implement more thorough validation)
        if User.objects.filter(username=username).exists():
            messages.warning(request, ("Username is already taken."))
            return redirect("register")
        if User.objects.filter(email=email).exists():
            messages.warning(request, ("An account with this email already exists."))
            return redirect("register")

        # Create a new user
        try:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
            )
            user.save()
            messages.success(request, ("Registration successful! You can now log in."))
            return redirect("login")
        except forms.ValidationError as e:
            messages.warning(request, ("Invalid input: ") + str(e))
            return redirect("register")

    return render(request, "register.html")


def create_superuser_view(request):
    User.objects.create_superuser("admin", "admin@example.com", "R@123")
    return HttpResponse("Superuser created successfully!")
