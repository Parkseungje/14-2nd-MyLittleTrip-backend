import json

from django.views import View
from django.http import JsonResponse
from rest_framework.views import APIView

from .models import Reservation
from serializers import ReservationSerializer

from user.utils import Login_decorator

class ReservationListView(APIView):

    @Login_decorator
    def post(self, request):
        data = json.loads(request.body)

        serializer = ReservationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)

    @Login_decorator
    def get(self, request):
        reservation = Reservation.objects.all()
        serializer = ReservationSerializer(reservation, many=True)
        return JsonResponse({'data': serializer.data}, status=200)

class Reservation(APIView):

    @Login_decorator
    def get(self, request, pk):
        pass

    @Login_decorator
    def patch(self, request, pk):
        pass

    @Login_decorator
    def delete(self, request, pk):
        reservation = Reservation.objects.get(id=pk)
