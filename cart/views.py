from django.shortcuts import redirect, render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import logging
from django.contrib.auth.decorators import login_required


def cart_summary(request):
    """Handles displaying the cart summary."""
    cart = Cart(request)
    return render(request, "cart_summary.html", {"cart": cart})


from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib import messages


def cart_add(request):
    if request.method == "POST" and request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        quantity = int(
            request.POST.get("quantity", 1)
        )  # Default to 1 if quantity is not provided
        product = get_object_or_404(Product, id=product_id)

        cart = Cart(request)
        cart.add(product=product, quantity=quantity)

        cart_quantity = len(cart)

        return JsonResponse(
            {
                "success": True,
                "qty": cart_quantity,
                "product_name": product.name,
                "quantity_added": quantity,
            }
        )

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
        messages.success(request, f"{product.name} has been removed from your cart.")
        # Redirect to the cart view after deletion
        return redirect("cart_summary")  # Change 'cart_detail' to your actual view name

    return HttpResponseBadRequest("Invalid request method or missing action")


def cart_update(request):
    if request.method == "POST" and request.POST.get("action") == "post":
        product_id = request.POST.get("product_id")
        quantity = request.POST.get("quantity")

        if not product_id or not quantity:
            messages.success(request, "Missing product_id or quantity.")
            return messages

        try:
            product_id = int(product_id)
            quantity = int(quantity)
        except (ValueError, TypeError):
            messages.success(request, "Missing product_id or quantity.")
            return messages

        product = get_object_or_404(Product, id=product_id)
        cart = Cart(request)
        cart.add(product=product, quantity=quantity, override_quantity=True)
        messages.success(request, f"Updated {product.name} quantity to {quantity}.")
        # Redirect to the cart view after update
        return redirect("cart_summary")  # Change 'cart_detail' to your actual view name

    messages.success(request, "Invalid request method or missing action")
    return messages


def checkout(request):
    return render(request, "checkout.html")


def input_view(request):
    if request.method == "POST":
        user_input = request.POST.get("user_input")
        response_message = f"You entered: {user_input}"  # Your processing logic here
        return JsonResponse({"message": response_message})
    return render(request, "myapp/index.html")


def payment(request):
    return render(request, "payment.html")


@csrf_exempt
@login_required
def clear_cart(request):
    if request.method == "POST":
        # Clear the cart session
        if "cart" in request.session:
            del request.session["cart"]
            request.session.modified = True
            return JsonResponse(
                {
                    "status": "success",
                    "message": "Cart cleared successfully!",
                    "cart_count": 0,
                }
            )
        else:
            return JsonResponse(
                {"status": "error", "message": "Cart is already empty."}, status=400
            )
    else:
        return JsonResponse(
            {"status": "error", "message": "Invalid request method."}, status=405
        )
