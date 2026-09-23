from django.contrib.auth.models import User
from django.db import OperationalError, ProgrammingError, models


class Customer(models.Model):
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  phone_number = models.CharField(max_length=20)

  def __str__(self):
    return f"{self.first_name} {self.last_name}"


class Order(models.Model):
  customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
  username = models.CharField(max_length=100)
  review_text = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.username} - {self.review_text[:20]}"


from django.contrib.auth import get_user_model

User = get_user_model()

try:
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'Ziri@gmail.com', 'python')
except Exception:
    pass