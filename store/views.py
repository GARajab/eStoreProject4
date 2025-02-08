from django.shortcuts import render, redirect
from .models import Category, Product
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms


def home(request):
    products = Product.objects.all()
    return render(request, "home.html", {"products": products})


def about(request):
    return render(request, "about.html", {})


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You Are Logged In Successfully"))
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
        messages.error(request, ("This Category Is Not Available"))
        return redirect("home")


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, "product.html", {"product": product})


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, ("You Have Registered Successfully!!"))
                return redirect("home")
        else:
            messages.error(
                request, ("Sorry There Was Something Wrong, Please Try Again!!")
            )
            return redirect("register")

    return render(request, "register.html", {"form": form})
