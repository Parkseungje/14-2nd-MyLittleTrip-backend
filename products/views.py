import json
from django.views import View
from django.http  import request, JsonResponse
from .models      import Product, Region, Airplane, SeatType
import datetime

class ProductListView(View):
    def get(self, request):
        from_region = request.GET.get('departure_region')
        to_region   = request.GET.get('arrive_region')
        from_date   = request.GET.get('departure_date')
        date_list   = [int(i) for i in from_date.split('-')]
        products    = Product.objects.select_related('airplane__from_region').filter(airplane__from_region__name = from_region,
                                                                                     airplane__to_region__name = to_region,
                                                                                     airplane__from_date__contains = datetime.date(date_list[0],
                                                                                                                                   date_list[1],
                                                                                                                                   date_list[2]))
        products_list = [
            {
                'from_region_name'      : product.airplane.from_region.name,
                'from_region_code'      : product.airplane.from_region.region_code,
                'from_region_image_url' : product.airplane.from_region.image_url,
                'to_region_name'        : product.airplane.to_region.name,
                'to_region_code'        : product.airplane.to_region.region_code,
                'to_region_image_url'   : product.airplane.to_region.image_url,
                'from_date'             : product.airplane.from_date.strftime("%Y-%m-%d-%H-%M-%s"),
                'to_date'               : product.airplane.to_date.strftime("%Y-%m-%d-%H-%M-%s"),
                'airplane_number'       : product.airplane.airplane_numbers,
                'airline_name'          : product.airplane.airline.name,
                'airline_url'           : product.airplane.airline.image_url,
                'price'                 : product.price,
                'seat_type'             : product.seat_type.name,
                'remaining_seat'        : product.remaining_seat,
                'total_seats'           : product.total_seats
            } for product in products
        ]
        return JsonResponse({'products_list' : products_list}, status=200)

    def post(self, request):
        data = json.loads(request.body)
        Product.objects.create(id=data['id'],
                               airplane=Airplane.objects.get(airplane_numbers=data['airplane']),
                               price=data['price'],
                               seat_type=SeatType.objects.get(name=data['seat_type']),
                               remaining_seat=data['remaining_seat'],
                               total_seats=data['total_seats'])
        return JsonResponse({'message':'create_success'}, status=200)


class ProductView(View):
    def delete(self, request, pk):
        delete_products = Product.objects.get(id=pk)
        delete_products.delete()

        return JsonResponse({'message':'delete_success'}, status=200)

    def patch(self, request, pk):
        data = json.loads(request.body)
        product = Product.objects.get(id=pk)
        product.seat_type.name = data['change_seat']
        product.save()
        return JsonResponse({'message':'update_success'}, status=200)

    
