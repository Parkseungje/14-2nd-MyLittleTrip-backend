from rest_framework import serializers

from products.models import Airline, Airplane, Product, Region, SeatType

class SeatTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model  = SeatType
        fields = ('name','image_url')

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
    airplane = AirplaneSerializer()

    class Meta:
        model  = Product
        fields = '__all__'
