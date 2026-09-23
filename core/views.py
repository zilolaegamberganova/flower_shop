from django.shortcuts import render, redirect, get_object_or_404
from products.models import Category, Product
from .models import Customer, Order
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from . import forms
from . import services
from products.filters import ProductFilter

def home_page(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    ctx = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'dashboard/home.html', ctx)

def login_required_decarator(func):
    return login_required(func, login_url='login_page')

def main_dashboard(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    customers = Customer.objects.all()
    orders = Order.objects.all()
    categories_products = []

    table_list = services.get_table() if hasattr(services, 'get_table') else []

    for category in categories:
        categories_products.append({
            "category": category.title,
            "product": Product.objects.filter(category_id=category.id).count()
        })

    ctx = {
        "counts": {
            "categories": len(categories),
            "products": len(products),
            "customers": len(customers),
            "orders": len(orders),
        },
        "categories_products": categories_products,
        "table_list": table_list,
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

def logout_page(request):
    logout(request)
    return redirect('login_page')

def user_list(request):
    users = Customer.objects.all()
    return render(request, "dashboard/user/list.html", {'users': users})

def user_create(request):
    model = Customer()
    form = forms.UserForm(request.POST or None, instance=model)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('user_list')

    ctx = {'model': model, 'form': form}
    return render(request, 'dashboard/user/form.html', ctx)

def user_edit(request, pk):
    model = get_object_or_404(Customer, pk=pk)
    form = forms.UserForm(request.POST or None, instance=model)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('user_list')

    ctx = {'model': model, 'form': form}
    return render(request, 'dashboard/user/form.html', ctx)

def user_delete(request, pk):
    model = get_object_or_404(Customer, pk=pk)
    model.delete()
    return redirect("user_list")

def category_list(request):
    categories = Category.objects.all()
    return render(request, "dashboard/category/list.html", {'categories': categories})

def category_create(request):
    model = Category()
    form = forms.CategoryForm(request.POST or None, instance=model)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('category_list')

    ctx = {'model': model, 'form': form}
    return render(request, 'dashboard/category/form.html', ctx)

def category_edit(request, pk):
    model = get_object_or_404(Category, pk=pk)
    form = forms.CategoryForm(request.POST or None, instance=model)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('category_list')

    ctx = {'model': model, 'form': form}
    return render(request, 'dashboard/category/form.html', ctx)

def category_delete(request, pk):
    model = get_object_or_404(Category, pk=pk)
    model.delete()
    return redirect("category_list")

def product_list(request):
    products = Product.objects.all()
    product_filter = ProductFilter(request.GET, queryset=products)
    return render(request, "dashboard/product_list.html", {'products': products, 'filter': product_filter})

def product_create(request):
    model = Product()
    form = forms.ProductForm(request.POST or None, request.FILES or None, instance=model)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('product_list')

    ctx = {'model': model, 'form': form}
    return render(request, 'dashboard/product_list.html', ctx)

def product_edit(request, pk):
    model = get_object_or_404(Product, pk=pk)
    form = forms.ProductForm(request.POST or None, request.FILES or None, instance=model)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('product_list')

    ctx = {'model': model, 'form': form}
    return render(request, 'dashboard/product_list.html', ctx)

def product_delete(request, pk):
    model = get_object_or_404(Product, pk=pk)
    model.delete()
    return redirect("product_list")

def order_list(request):
    orders = Order.objects.all()
    return render(request, "dashboard/order/list.html", {'orders': orders})

def customer_order_list(request, id):
    customer_orders = services.get_order_by_user(id=id) if hasattr(services, 'get_order_by_user') else []
    return render(request, "dashboard/customer_order/login.html", {'customer_orders': customer_orders})

def orderproduct_list(request, id):
    productorders = services.get_product_by_order(id=id) if hasattr(services, 'get_product_by_order') else []
    return render(request, "dashboard/productorder/login.html", {'productorders': productorders})

def order_create(request):
    form = forms.OrderForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('order_list')
    return render(request, 'dashboard/order/form.html', {'form': form})