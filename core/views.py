import json
import random

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from . import forms, services
from .models import Category, Customer, Order, OrderItem, Product, Review


def login_required_decorator(func):
    return login_required(func, login_url="login_page")


def home_page(request):
    ctx = {
        "products": Product.objects.all(),
        "categories": Category.objects.all(),
        "reviews": Review.objects.all().order_by("-id"),
    }
    return render(request, "dashboard/home.html", ctx)


def login_page(request):
    if request.user.is_authenticated:
        return redirect("main_dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect("main_dashboard")

    return render(request, "dashboard/login.html")


@login_required_decorator
def logout_page(request):
    logout(request)
    return redirect("login_page")


def checkout_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get("name")
            phone = data.get("phone")
            address = data.get("address", "")
            items = data.get("items", [])

            if not name or not phone:
                return JsonResponse(
                    {"status": "error", "message": "Ism va telefon kiritish shart!"},
                    status=400,
                )

            name_parts = name.strip().split()
            first_name = name_parts[0]
            last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

            customer, _ = Customer.objects.update_or_create(
                phone_number=phone,
                defaults={"first_name": first_name, "last_name": last_name}
            )

            total_price = sum(float(item.get("price", 0)) * int(item.get("quantity", 1)) for item in items)
            delivery_days = random.randint(1, 10)

            order = Order.objects.create(
                customer=customer,
                phone=phone,
                address=address,
                total_price=total_price,
                status="delivering",
            )

            for item in items:
                product_id = item.get("id")
                qty = int(item.get("quantity", 1))
                price = float(item.get("price", 0))

                product = None
                if product_id:
                    product = Product.objects.filter(pk=product_id).first()
                if not product and item.get("title"):
                    product = Product.objects.filter(title__iexact=item.get("title")).first()

                if product:
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=qty,
                        price=price
                    )

            return JsonResponse(
                {"status": "success", "message": f"Buyurtmangiz qabul qilindi! {delivery_days} kunda yetkaziladi."}
            )
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Noto'g'ri so'rov"}, status=400)


@login_required_decorator
def main_dashboard(request):
    categories = Category.objects.annotate(product_count=Count("product"))

    chart_categories = [cat.title if hasattr(cat, 'title') else getattr(cat, 'name', 'Kategoriya') for cat in categories]
    chart_products = [cat.product_count for cat in categories]

    ctx = {
        "counts": {
            "categories": categories.count(),
            "products": Product.objects.count(),
            "customers": Customer.objects.count(),
            "orders": Order.objects.count(),
        },
        "chart_categories": json.dumps(chart_categories if chart_categories else ["Atirgullar", "Lolalar", "Xonaki"]),
        "chart_products": json.dumps(chart_products if chart_products else [12, 19, 7]),
        "monthly_labels": json.dumps(["Yan", "Fev", "Mar", "Apr", "May", "Iyun", "Iyul"]),
        "monthly_data": json.dumps([120, 250, 180, 390, 420, 510, 680]),
        "orders": Order.objects.select_related("customer").prefetch_related("items__product").order_by("-id")[:10],
    }
    return render(request, "dashboard/index.html", ctx)


@login_required_decorator
def user_list(request):
    return render(
        request, "dashboard/user/list.html", {"users": Customer.objects.all()}
    )


@login_required_decorator
def user_create(request):
    form = forms.UserForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("user_list")
    return render(request, "dashboard/user/form.html", {"form": form})


@login_required_decorator
def user_edit(request, pk):
    model = get_object_or_404(Customer, pk=pk)
    form = forms.UserForm(request.POST or None, instance=model)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("user_list")
    return render(
        request, "dashboard/user/form.html", {"model": model, "form": form}
    )


@login_required_decorator
def user_delete(request, pk):
    get_object_or_404(Customer, pk=pk).delete()
    return redirect("user_list")


@login_required_decorator
def category_list(request):
    return render(
        request,
        "dashboard/category/list.html",
        {"categories": Category.objects.all()},
    )


@login_required_decorator
def category_create(request):
    form = forms.CategoryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("category_list")
    return render(request, "dashboard/category/form.html", {"form": form})


@login_required_decorator
def category_edit(request, pk):
    model = get_object_or_404(Category, pk=pk)
    form = forms.CategoryForm(request.POST or None, instance=model)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("category_list")
    return render(
        request, "dashboard/category/form.html", {"model": model, "form": form}
    )


@login_required_decorator
def category_delete(request, pk):
    get_object_or_404(Category, pk=pk).delete()
    return redirect("category_list")


@login_required_decorator
def product_list(request):
    return render(
        request,
        "dashboard/product_list.html",
        {"products": Product.objects.all()},
    )


@login_required_decorator
def product_create(request):
    form = forms.ProductForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("product_list")
    return render(
        request,
        "dashboard/product_list.html",
        {"form": form, "products": Product.objects.all()},
    )


@login_required_decorator
def product_edit(request, pk):
    model = get_object_or_404(Product, pk=pk)
    form = forms.ProductForm(
        request.POST or None, request.FILES or None, instance=model
    )
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("product_list")
    return render(
        request,
        "dashboard/product_list.html",
        {"model": model, "form": form, "products": Product.objects.all()},
    )


@login_required_decorator
def product_delete(request, pk):
    get_object_or_404(Product, pk=pk).delete()
    return redirect("product_list")


@login_required_decorator
def order_list(request):
    orders = Order.objects.select_related('customer').prefetch_related('items__product').all().order_by('-id')
    return render(
        request, "dashboard/order/list.html", {"orders": orders}
    )


@login_required_decorator
def order_create(request):
    form = forms.OrderForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("order_list")
    return render(request, "dashboard/order/form.html", {"form": form})


@login_required_decorator
def customer_order_list(request, id):
    orders = getattr(services, "get_order_by_user", lambda id: [])(id=id)
    return render(
        request,
        "dashboard/customer_order/login.html",
        {"customer_orders": orders},
    )


@login_required_decorator
def orderproduct_list(request, id):
    products = getattr(services, "get_product_by_order", lambda id: [])(id=id)
    return render(
        request,
        "dashboard/productorder/login.html",
        {"productorders": products},
    )


def buy_now(request, product_id):
    if request.method == "POST":
        try:
            product = get_object_or_404(Product, pk=product_id)
            data = {}
            if request.body:
                try:
                    data = json.loads(request.body)
                except Exception:
                    pass

            phone = data.get("phone")
            name = data.get("name")
            quantity = int(data.get("quantity", 1))

            if not phone or not name:
                return JsonResponse({"status": "error", "message": "Ism va telefon raqam kiritilishi shart!"},
                                    status=400)

            name_parts = name.strip().split()
            first_name = name_parts[0]
            last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

            customer, _ = Customer.objects.update_or_create(
                phone_number=phone,
                defaults={"first_name": first_name, "last_name": last_name}
            )

            order = Order.objects.create(
                customer=customer,
                phone=phone,
                address=data.get("address", "Manzil ko'rsatilmadi"),
                total_price=product.price * quantity,
                status="delivering"
            )

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )

            delivery_days = random.randint(1, 10)

            return JsonResponse(
                {
                    "status": "success",
                    "message": f"'{product.title}' muvaffaqiyatli xarid qilindi! Buyurtmangiz {delivery_days} kunda yetkaziladi.",
                }
            )
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse(
        {"status": "error", "message": "Noto'g'ri so'rov!"}, status=400
    )


def add_comment(request):
    if request.method == "POST":
        username = request.POST.get("username")
        text = request.POST.get("text")
        if username and text:
            Review.objects.create(username=username, review_text=text)
            return JsonResponse(
                {"status": "success", "username": username, "text": text}
            )
    return JsonResponse(
        {"status": "error", "message": "Maydonlarni to'ldiring!"}, status=400
    )