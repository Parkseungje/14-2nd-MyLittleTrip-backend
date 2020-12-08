import json
import datetime

from django.views import View
from django.http  import request, JsonResponse
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from .models      import Product, Region, Airplane, Airline
from products.serializers  import ProductSerializer, ProductListQuerySerializer

class ProductListView(APIView):

    @swagger_auto_schema(
        query_serializer=ProductListQuerySerializer,
        responses={200: ProductSerializer(many=True)},
        tags=['Products'],
    )
    def get(self, request):

        from_region = request.GET.get('departure_region', None)
        to_region   = request.GET.get('arrival_region', None)
        from_date   = request.GET.get('departure_date', None)
        offset      = int(request.GET.get('offset', 0))
        limit       = int(request.GET.get('limit', 20))
        get_airline = request.GET.getlist('airline', None)
        get_seat    = request.GET.getlist('seat', None)
        
        q = Q()  # Q()는 쿼리이다.
        if from_region:
            q.add(Q(airplane__from_region__name=from_region), Q.AND) # q.add는(Q(), Q.AND)는 다른 값이 None이여도 남은 값들끼리의 AND값을 필터링해준다.
        
        if to_region:
            q.add(Q(airplane__to_region__name=to_region), Q.AND)
        
        if from_date:
            date = [int(i) for i in from_date.split('-')]
            q.add(Q(airplane__from_date__contains=datetime.date(date[0],date[1],date[2])), Q.AND)
            
        products = Product.objects.select_related('airplane__from_region').filter(q).exclude(Q(airplane__airline__name__in=get_airline)|Q(seat_type__name__in=get_seat)).order_by('price')[offset:offset+limit]
        serializer = ProductSerializer(products, many=True) #many=True는 다수의 쿼리가 허용될때 사용
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    
class ProductView(APIView):
    
    def get(self, request, pk):
        try:
            get_products = Product.objects.get(id=pk)
            serializer   = ProductSerializer(get_products)
            return Response({'data':serializer.data}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'message':'DoesNotExist'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            delete_products = Product.objects.get(id=pk)
            delete_products.delete()
            return Response({'message':'delete_success'}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'message':'DoesNotExist'}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            data                   = json.loads(request.body)
            product                = Product.objects.get(id=pk)
            product.seat_type.name = data['change_seat']
            product.save()
            serializer             = ProductSerializer(product)
            return Response({'data':serializer.data}, status=status.HTTP_200_OK)

        except KeyError:
            return Response({'message':'KEY_ERROR'}, status=status.HTTP_400_BAD_REQUEST)

            
        
