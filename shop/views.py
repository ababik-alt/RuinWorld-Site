import re
from decimal import Decimal

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import Product, Order
from .rcon import execute_commands

NICK_RE = re.compile(r"^[A-Za-z0-9_]{3,16}$")


def index(request):
    products = Product.objects.filter(active=True)
    return render(request, "index.html", {"products": products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, active=True)
    return render(request, "product.html", {"product": product})


def checkout(request, slug):
    product = get_object_or_404(Product, slug=slug, active=True)

    if request.method == "POST":
        player = request.POST.get("player", "").strip()

        if not NICK_RE.fullmatch(player):
            messages.error(request, "Ник должен быть от 3 до 16 символов: A-Z, a-z, 0-9, _.")
            return redirect("checkout", slug=slug)

        if product.is_currency:
            try:
                quantity = int(request.POST.get("quantity", product.min_quantity))
            except (TypeError, ValueError):
                quantity = 0

            if quantity < product.min_quantity or quantity > product.max_quantity:
                messages.error(
                    request,
                    f"Количество должно быть от {product.min_quantity} до {product.max_quantity}."
                )
                return redirect("checkout", slug=slug)

            amount = (product.price_per_unit * Decimal(quantity)).quantize(Decimal("0.01"))
        else:
            quantity = 1
            amount = product.price

        order = Order.objects.create(
            player=player,
            product=product,
            quantity=quantity,
            amount=amount,
        )
        return redirect("ruinpay", order_id=order.id)

    return render(request, "checkout.html", {"product": product})


def ruinpay(request, order_id):
    order = get_object_or_404(Order.objects.select_related("product"), id=order_id)

    if order.status == Order.Status.DELIVERED:
        return redirect("success", order_id=order.id)

    if request.method == "POST":
        method = request.POST.get("method", "blik")
        return redirect("ruinpay_processing", order_id=order.id, method=method)

    return render(request, "ruinpay.html", {"order": order})


def ruinpay_processing(request, order_id, method):
    order = get_object_or_404(Order.objects.select_related("product"), id=order_id)

    if order.status == Order.Status.DELIVERED:
        return redirect("success", order_id=order.id)

    allowed = {"blik", "card", "transfer"}
    if method not in allowed:
        method = "blik"

    return render(request, "ruinpay_processing.html", {
        "order": order,
        "method": method,
    })


def ruinpay_finish(request, order_id):
    order = get_object_or_404(Order.objects.select_related("product"), id=order_id)

    if order.status == Order.Status.DELIVERED:
        return redirect("success", order_id=order.id)

    try:
        commands = order.product.command_list(order.player, order.quantity)
        results = execute_commands(commands)

        order.status = Order.Status.DELIVERED
        order.paid_at = timezone.now()
        order.delivered_at = timezone.now()
        order.rcon_log = "\n\n".join(results)
        order.save(update_fields=["status", "paid_at", "delivered_at", "rcon_log"])
    except Exception as exc:
        order.status = Order.Status.FAILED
        order.rcon_log = f"RCON error: {exc}"
        order.save(update_fields=["status", "rcon_log"])
        messages.error(request, "Не удалось выдать товар. Проверь RCON.")
        return redirect("order", order_id=order.id)

    return redirect("success", order_id=order.id)


def success(request, order_id):
    order = get_object_or_404(Order.objects.select_related("product"), id=order_id)
    return render(request, "success.html", {"order": order})


def order_detail(request, order_id):
    order = get_object_or_404(Order.objects.select_related("product"), id=order_id)
    return render(request, "order.html", {"order": order})
