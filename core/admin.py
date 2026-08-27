from django.contrib import admin
from .models import Category,Customer,Product,Review,Order

admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Order)
