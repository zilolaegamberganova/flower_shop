from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='flowers/', blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name or "Unnamed Product"