from django.shortcuts import render, redirect
from core.models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from . import forms
from . import services


def login_required_decorator(func):
    return login_required(func, login_url='login_page')


def home_page(request):
    products = Product.objects.all() if 'Product' in globals() else []
    categories = Category.objects.all() if 'Category' in globals() else []
    reviews = Review.objects.all() if 'Review' in globals() else []

    ctx = {
        'products': products,
        'categories': categories,
        'reviews': reviews,
    }
    return render(request, 'index.html', ctx)


@login_required_decorator
def main_dashboard(request):
    categories = Category.objects.all() if 'Category' in globals() else []
    categories_products = []

    for category in categories:
        categories_products.append({
            "category": getattr(category, 'title', getattr(category, 'name', 'Kategoriya')),
            "product": Product.objects.filter(category_id=category.id).count() if 'Product' in globals() else 0
        })

    ctx = {
        "counts": {
            "categories": Category.objects.count() if 'Category' in globals() else 0,
            "products": Product.objects.count() if 'Product' in globals() else 0,
            "customers": Customer.objects.count() if 'Customer' in globals() else 0,
            "orders": Order.objects.count() if 'Order' in globals() else 0,
            "reviews": Review.objects.count() if 'Review' in globals() else 0,
        },
        "categories_products": categories_products,
        "orders": Order.objects.all() if 'Order' in globals() else [],
    }
    return render(request, 'dashboard/index.html', ctx)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('main_dashboard')

    if request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main_dashboard')

    return render(request, 'dashboard/login.html')


@login_required_decorator
def logout_page(request):
    logout(request)
    return redirect('login_page')


@login_required_decorator
def category_list(request):
    categories = Category.objects.all() if 'Category' in globals() else []
    return render(request, "dashboard/category/list.html", {'categories': categories})



@login_required_decorator
def product_list(request):
    products = Product.objects.all() if 'Product' in globals() else []
    return render(request, "dashboard/product/list.html", {'products': products})


@login_required_decorator
def user_list(request):
    users = Customer.objects.all() if 'Customer' in globals() else []
    return render(request, "dashboard/user/list.html", {'users': users})



@login_required_decorator
def order_list(request):
    orders = Order.objects.all() if 'Order' in globals() else []
    return render(request, "dashboard/order/list.html", {'orders': orders})