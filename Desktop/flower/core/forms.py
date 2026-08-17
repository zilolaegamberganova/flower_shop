from django import forms
from core.models import Category, Product, Customer, Order

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        widgets = {
            "title": forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            "title": forms.TextInput(attrs={'class': 'form-control'}),
            "description": forms.TextInput(attrs={'class': 'form-control'}),
            "cost": forms.TextInput(attrs={'class': 'form-control'}),
            "price": forms.TextInput(attrs={'class': 'form-control'}),
            "category": forms.Select(attrs={'class': 'form-control'}),
            "image": forms.FileInput(attrs={
                'class': 'form-control',
                'onchange': 'loadFile(event)'
            }),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"
        widgets = {
            "first_name": forms.TextInput(attrs={'class': 'form-control'}),
            "last_name": forms.TextInput(attrs={'class': 'form-control'}),
            "phone_number": forms.TextInput(attrs={'class': 'form-control'}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["customer"]
        widgets = {"customer": forms.Select(attrs={"class": "form-control"})}
