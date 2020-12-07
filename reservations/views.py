import json

from django.views import View
from django.http import JsonResponse
from rest_framework.views import APIView

from .models import Reservation
from serializers import ReservationSerializer

from users.utils import Login_decorator

class ReservationListView(APIView):
    @Login_decorator
    def post(self, request):
        data = json.loads(request.body)
        data['user_id'] = request.user.id 
        serializer = ReservationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)

    @Login_decorator
    def get(self, request):
        reservation = Reservation.objects.get(user=request.user)
        serializer = ReservationSerializer(reservation, many=True)
        return JsonResponse({'data': serializer.data}, status=200)

class Reservation(APIView):
    @Login_decorator
    def get_reservation(self, pk):
        try:
            return JsonResponse(Reservation.objects.get(id=pk))
        except Reservation.DoesNotExist:
            return JsonResponse({'message': 'Reservation Dose Not Exist'}, status=400)

    def get(self, request, pk):
        serializer = ReservationSerializer(get_reservation(pk))
        return JsonResponse({'data': serializer.data}, status=200)

    def patch(self, request, pk):
        data = json.loads(request.body)
        serializer = ReservationSerializer(get_reservation(pk), data=data, partial=True)
        return JsonResponse({'data': serializer.data}, status=200)

    def delete(self, request, pk):
        reservation = Reservation.objects.get(id=pk)
        reservation.delete()
        return JsonResponse(status=204)
