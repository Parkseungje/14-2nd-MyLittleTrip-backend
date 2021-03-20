from rest_framework import serializers

from .models import Reservation
from products.models import Product
from products.serializers import ProductSerializer

class ReservationSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True, read_only=True)

    class Meta:
        model  = Reservation
        fields = ('id', 'head_count', 'product', 'user')

class ReservationCreateSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Product.objects.all())

    class Meta:
        model = Reservation
        fields = ('id', 'head_count', 'product', 'user')
