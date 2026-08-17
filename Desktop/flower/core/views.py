import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count
from .models import Category, Product, Customer, Order
from . import forms, services


def login_required_decorator(func):
    return login_required(func, login_url='login_page')


def home_page(request):
    ctx = {
        'products': Product.objects.all(),
        'categories': Category.objects.all(),
    }
    return render(request, 'dashboard/home.html', ctx)


def checkout_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get('name')
            phone = data.get('phone')
            address = data.get('address')
            items = data.get('items', [])

            if not name or not phone:
                return JsonResponse({"status": "error", "message": "Ism va telefon kiritilishi shart!"}, status=400)

            # Mijozni yaratish yoki mavjudini olish
            customer, created = Customer.objects.get_or_create(
                phone=phone,
                defaults={'name': name, 'address': address}
            )

            # Buyurtma umumiy summasini hisoblash
            total_price = sum(float(item.get('price', 0)) for item in items)

            # Buyurtmani saqlash
            order = Order.objects.create(
                customer=customer,
                address=address,
                total_price=total_price
            )

            return JsonResponse({"status": "success", "message": "Buyurtmangiz qabul qilindi!"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Noto'g'ri so'rov"}, status=400)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('main_dashboard')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('main_dashboard')

    return render(request, 'dashboard/login.html')


@login_required_decorator
def logout_page(request):
    logout(request)
    return redirect('login_page')


@login_required_decorator
def main_dashboard(request):
    categories = Category.objects.annotate(product_count=Count('product'))

    ctx = {
        "counts": {
            "categories": categories.count(),
            "products": Product.objects.count(),
            "customers": Customer.objects.count(),
            "orders": Order.objects.count(),
        },
        "categories_products": [
            {"category": cat.title, "product": cat.product_count}
            for cat in categories
        ],
        "table_list": getattr(services, 'get_table', lambda: [])(),
    }
    return render(request, 'dashboard/index.html', ctx)


# --- USERS / CUSTOMERS ---
@login_required_decorator
def user_list(request):
    return render(request, "dashboard/user/list.html", {'users': Customer.objects.all()})


@login_required_decorator
def user_create(request):
    form = forms.UserForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('user_list')
    return render(request, 'dashboard/user/form.html', {'form': form})


@login_required_decorator
def user_edit(request, pk):
    model = get_object_or_404(Customer, pk=pk)
    form = forms.UserForm(request.POST or None, instance=model)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('user_list')
    return render(request, 'dashboard/user/form.html', {'model': model, 'form': form})


@login_required_decorator
def user_delete(request, pk):
    get_object_or_404(Customer, pk=pk).delete()
    return redirect("user_list")


# --- CATEGORIES ---
@login_required_decorator
def category_list(request):
    return render(request, "dashboard/category/list.html", {'categories': Category.objects.all()})


@login_required_decorator
def category_create(request):
    form = forms.CategoryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('category_list')
    return render(request, 'dashboard/category/form.html', {'form': form})


@login_required_decorator
def category_edit(request, pk):
    model = get_object_or_404(Category, pk=pk)
    form = forms.CategoryForm(request.POST or None, instance=model)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('category_list')
    return render(request, 'dashboard/category/form.html', {'model': model, 'form': form})


@login_required_decorator
def category_delete(request, pk):
    get_object_or_404(Category, pk=pk).delete()
    return redirect("category_list")


# --- PRODUCTS ---
@login_required_decorator
def product_list(request):
    return render(request, "dashboard/product_list.html", {'products': Product.objects.all()})


@login_required_decorator
def product_create(request):
    form = forms.ProductForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, 'dashboard/product_list.html', {'form': form, 'products': Product.objects.all()})


@login_required_decorator
def product_edit(request, pk):
    model = get_object_or_404(Product, pk=pk)
    form = forms.ProductForm(request.POST or None, request.FILES or None, instance=model)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, 'dashboard/product_list.html',
                  {'model': model, 'form': form, 'products': Product.objects.all()})


@login_required_decorator
def product_delete(request, pk):
    get_object_or_404(Product, pk=pk).delete()
    return redirect("product_list")


# --- ORDERS ---
@login_required_decorator
def order_list(request):
    return render(request, "dashboard/order/list.html", {'orders': Order.objects.all()})


@login_required_decorator
def order_create(request):
    form = forms.OrderForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('order_list')
    return render(request, 'dashboard/order/form.html', {'form': form})


@login_required_decorator
def customer_order_list(request, id):
    orders = getattr(services, 'get_order_by_user', lambda id: [])(id=id)
    return render(request, "dashboard/customer_order/login.html", {'customer_orders': orders})


@login_required_decorator
def orderproduct_list(request, id):
    products = getattr(services, 'get_product_by_order', lambda id: [])(id=id)
    return render(request, "dashboard/productorder/login.html", {'productorders': products})


def buy_now(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, pk=product_id)
        return JsonResponse({"status": "success", "message": f"'{product.title}' muvaffaqiyatli xarid qilindi!"})
    return JsonResponse({"status": "error", "message": "Noto'g'ri so'rov!"}, status=400)


def add_comment(request):
    if request.method == "POST":
        username = request.POST.get('username')
        text = request.POST.get('text')
        if username and text:
            return JsonResponse({"status": "success", "username": username, "text": text})
    return JsonResponse({"status": "error", "message": "Maydonlarni to'ldiring!"}, status=400)