from rest_framework import serializers

from .models import Reservation
from products.serializers import ProductSerializer

class ReservationSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True, read_only=True)

    class Meta:
        model  = Reservation
        fields = ('id', 'head_count', 'product', 'user')
