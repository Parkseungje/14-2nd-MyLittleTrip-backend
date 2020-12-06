import json
import datetime

from django.views import View
from django.http  import request, JsonResponse
from django.db.models import Q
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from .models      import Product, Region, Airplane
from serializers  import ProductSerializer, ProductListQuerySerializer

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

        q = Q()

        if from_region:
            q.add(Q(airplane__from_region__name=from_region), Q.AND)

        if to_region:
            q.add(Q(airplane__to_region__name=to_region), Q.AND)

        if from_date:
            date = [int(i) for i in from_date.split('-')]
            q.add(Q(airplane__from_date__contains=datetime.date(date[0],date[1],date[2])), Q.AND)

        products = Product.objects.select_related('airplane__from_region').filter(q)[offset:offset+limit]
        serializer = ProductSerializer(products, many=True)
        return JsonResponse({'data': serializer.data}, status=200)
