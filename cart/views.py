from django.shortcuts import redirect, render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse, HttpResponseBadRequest


def cart_summary(request):
    """Handles displaying the cart summary."""
    cart = Cart(request)
    return render(request, "cart_summary.html", {"cart": cart})


def cart_add(request):
    """Handles adding a product to the cart via a POST request."""
    if request.method == "POST" and request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        product = get_object_or_404(Product, id=product_id)
        cart = Cart(request)
        cart.add(product=product)
        cart_quantity = len(cart)
        return JsonResponse({"qty": cart_quantity})

    return HttpResponseBadRequest("Invalid request method or missing action")


def cart_delete(request):
    if request.method == "POST" and request.POST.get("action") == "post":
        product_id = request.POST.get("product_id")
        if not product_id:
            return HttpResponseBadRequest("Missing product_id")

        try:
            product_id = int(product_id)
        except (ValueError, TypeError):
            return HttpResponseBadRequest("Invalid product_id")

        product = get_object_or_404(Product, id=product_id)
        cart = Cart(request)
        cart.remove(product)

        # Redirect to the cart view after deletion
        return redirect("cart_summary")  # Change 'cart_detail' to your actual view name

    return HttpResponseBadRequest("Invalid request method or missing action")


def cart_update(request):
    if request.method == "POST" and request.POST.get("action") == "post":
        product_id = request.POST.get("product_id")
        quantity = request.POST.get("quantity")

        if not product_id or not quantity:
            return HttpResponseBadRequest("Missing product_id or quantity")

        try:
            product_id = int(product_id)
            quantity = int(quantity)
        except (ValueError, TypeError):
            return HttpResponseBadRequest("Invalid product_id or quantity")

        product = get_object_or_404(Product, id=product_id)
        cart = Cart(request)
        cart.add(product=product, quantity=quantity, override_quantity=True)

        # Redirect to the cart view after update
        return redirect("cart_summary")  # Change 'cart_detail' to your actual view name

    return HttpResponseBadRequest("Invalid request method or missing action")
