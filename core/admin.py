from django.contrib import admin
from .models import Customer, Order, Review

admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Review)