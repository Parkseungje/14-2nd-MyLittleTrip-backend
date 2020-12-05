from rest_framework import serializers

from reservations.models import Reservation
from products.models import SeatType, Product, Airline,Airplane, Region

class SeatTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeatType
        fields = ('name',)

class AirlineSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Airline
        fields = ('name','image_url')

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Region
        fields = ('name','region_code')

class AirplaneSerializer(serializers.ModelSerializer):
    from_region = RegionSerializer()
    to_region   = RegionSerializer()
    airline     = AirlineSerializer()

    class Meta:
        model  =  Airplane
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    airplane  = AirplaneSerializer()
    seat_type = SeatTypeSerializer() 
    class Meta:
        model  = Product
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True, read_only=True)

    class Meta:
        model  = Reservation
        fields = ('id', 'head_count', 'product', 'user')

class ProductListQuerySerializer(serializers.Serializer):
    departure_region = serializers.CharField(help_text="출발 지역", required=False)
    arrival_region   = serializers.CharField(help_text="도착 지역", required=False)
    departure_date   = serializers.CharField(help_text="출발 날짜(YYYY-MM-DD)", required=False)
