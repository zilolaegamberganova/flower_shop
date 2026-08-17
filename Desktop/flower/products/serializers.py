from rest_framework import serializers
from .models import Product,Review,Category

class ReviewSerializer(serializers.ModelSerizlizer):
    class Meta:
        model=Review
        fields=['id','product', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['user']
