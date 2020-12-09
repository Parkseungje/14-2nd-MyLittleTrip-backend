import json

from django.views import View
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Reservation
from .serializers import ReservationSerializer, ReservationCreateSerializer

class ReservationListView(APIView):
    def post(self, request):
        data = json.loads(request.body)

        serializer = ReservationCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        reservation = Reservation.objects.all()
        serializer = ReservationSerializer(reservation, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
