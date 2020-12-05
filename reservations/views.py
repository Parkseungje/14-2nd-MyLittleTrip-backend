import json

from django.views import View
from django.http import JsonResponse
from rest_framework.views import APIView

from .models import Reservation
from serializers import ReservationSerializer

class ReservationListView(APIView):
    def post(self, request):
        data = json.loads(request.body)

        serializer = ReservationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)

    def get(self, request):
        reservation = Reservation.objects.all()
        serializer = ReservationSerializer(reservation, many=True)
        return JsonResponse({'data': serializer.data}, status=200)

