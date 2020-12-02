from django.test import TestCase, Client
from django.http import request
from .models     import SeatType, Region, Airline, Airplane, Product
import datetime
class ProductListTestCase(TestCase):
    def setUp(self):
        self.URL = '/products?departure_region=김포&arrive_region=울산&departure_date=2020-12-17'
        # 위 self.URL의 쿼리스트링은 get요청이 아닌 다른 요청이면 무시되어 url이 '/products' 상태가 된다
        self.client = Client()
        
        SeatType.objects.bulk_create(
            [
             SeatType(name='비즈니스석'), 
            ]
        )
        Region.objects.bulk_create(
            [
             Region(name='김포',region_code='GMP',image_url=''),
             Region(name='울산',region_code='USN',image_url='')
            ]
        )
        Airline.objects.bulk_create(
            [
             Airline(name='진에어',image_url='rud123213jkjdk'),
            ]
        )
        Airplane.objects.create(
                                airline=Airline.objects.get(name='진에어'),
                                from_region=Region.objects.get(name='김포'),
                                to_region=Region.objects.get(name='울산'),
                                from_date= datetime.datetime(2020, 12, 17, 10, 5, 00),
                                to_date= datetime.datetime(2020, 12, 17, 10, 6, 00),
                                airplane_numbers="KP665"
        )

        Product.objects.create(
           id = 1,
           airplane=Airplane.objects.all().first(),
           price=5000,
           seat_type=SeatType.objects.all().first(),
           remaining_seat =170, 
           total_seats=300
        )
        product = Product.objects.all().first()
        self.products_list = [
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
            'price'                 : str(product.price),
            'seat_type'             : product.seat_type.name,
            'remaining_seat'        : product.remaining_seat,
            'total_seats'           : product.total_seats
            }
        ]

    def tearDown(self):  # 해당 클래스의 테스트가 끝나고 자동으로 마지막으로 실행이 된다.
        del self.products_list
        SeatType.objects.all().delete()
        Region.objects.all().delete()
        Airline.objects.all().delete()
        Airplane.objects.all().delete()
        Product.objects.all().delete()

    def test_get_success(self):
        response = self.client.get(self.URL)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['products_list'], self.products_list)
    
    def test_create_success(self):
        request = {'id' : 4, 
                   'airplane' : 'KP665',
                   'price' : 2000,
                   'seat_type' : '비즈니스석',
                   'remaining_seat' : 120,
                   'total_seats' : 300}

        response = self.client.post(self.URL, request, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'],'create_success')


class ProductTestCase(TestCase):
    def setUp(self):
        self.delete_URL = '/products/2'
        self.patch_URL  = '/products/3'
        self.client = Client()
        
        SeatType.objects.bulk_create(
            [
             SeatType(name='비즈니스석'),
             SeatType(name='장규석'),
            ]
        )
        Region.objects.bulk_create(
            [
             Region(name='김포',region_code='GMP',image_url=''),
             Region(name='울산',region_code='USN',image_url='')
            ]
        )
        Airline.objects.bulk_create(
            [
             Airline(name='진에어',image_url='rud123213jkjdk'),
             Airline(name='아시아나', image_url='vkd1214ewer')
            ]
        )
        Airplane.objects.bulk_create(
                               [
                                Airplane(airline          = Airline.objects.get(name='진에어'),
                                         from_region      = Region.objects.get(name='김포'),
                                         to_region        = Region.objects.get(name='울산'),
                                         from_date        = datetime.datetime(2020, 12, 17, 10, 5, 00),
                                         to_date          = datetime.datetime(2020, 12, 17, 10, 6, 00),
                                         airplane_numbers = 'KP665'
                                        ),
                                Airplane(airline          = Airline.objects.get(name='아시아나'),
                                         from_region      = Region.objects.get(name = '울산'),
                                         to_region        = Region.objects.get(name = '김포'),
                                         from_date        = datetime.datetime(2020, 12, 20, 11, 8, 00),
                                         to_date          = datetime.datetime(2020, 12, 21, 7, 10, 00),
                                         airplane_numbers = 'SN775'
                                        )
                               ]
        )
        Product.objects.bulk_create(
            [
             Product(id             = 2,
                     airplane       = Airplane.objects.get(airline=Airline.objects.get(name='진에어')),
                     price          = 5000,
                     seat_type      = SeatType.objects.get(name='비즈니스석'),
                     remaining_seat = 170, 
                     total_seats    = 300
                    ),
             Product(id              = 3,
                    airplane        = Airplane.objects.get(airline=Airline.objects.get(name='아시아나')),
                    price           = 7000,
                    seat_type       = SeatType.objects.get(name='장규석'),
                    remaining_seat  = 100, 
                    total_seats     = 300
                   )
            ]
        )

    def test_delete_success(self):
        response = self.client.delete(self.delete_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'],'delete_success')

    def test_patch_success(self):
        request = {'change_seat' : '장규석'}
        
        response = self.client.patch(self.patch_URL, request, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'],'update_success')
    
    

