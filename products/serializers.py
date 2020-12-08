from rest_framework import serializers
from .models import SeatType, Product, Airline,Airplane, Region

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

class ProductListQuerySerializer(serializers.Serializer):
    departure_region = serializers.CharField(help_text="출발 지역", required=False) # required 필수인지 아닌지
    arrival_region   = serializers.CharField(help_text="도착 지역", required=False)
    departure_date   = serializers.DateField(help_text="출발 날짜(YYYY-MM-DD)", required=False)
    offset           = serializers.CharField(help_text="시작위치", required=False)
    limit            = serializers.CharField(help_text="리스트 갯수", required=False)
