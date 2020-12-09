import json

from django.test import TestCase, Client, TransactionTestCase

from .models import Reservation
from users.models import User
from products.models import Product, Airplane, Airline, Region, SeatType

class ReservationListViewTestCase(TransactionTestCase):
    def setUp(self):
        self.URL = '/reservations'
        self.client = Client()
        #Create User
        self.user = User.objects.create(email='user@gmail.com', name='user', password='12345678')
        #Create Airline
        self.airline = Airline.objects.create(name='아시아나')
        #Create Region
        self.region1 = Region.objects.create(name='군산')
        self.region2 = Region.objects.create(name='강남')
        #Create Airplane
        self.airplane1 = Airplane.objects.create(
            airline_id=self.airline.id,
            from_region_id=self.region1.id,
            to_region_id=self.region2.id,
            from_date='2020-12-03 02:08:00',
            to_date='2020-12-03 12:08:00',
            airplane_numbers='LCK920420'
        )
        self.airplane2 = Airplane.objects.create(
            airline_id=self.airline.id,
            from_region_id=self.region2.id,
            to_region_id=self.region1.id,
            from_date='2020-12-04 02:08:00',
            to_date='2020-12-04 12:08:00',
            airplane_numbers='YDG920420'
        )
        #Create SeatType
        self.seat_type = SeatType.objects.create(name='일반석')
        #Create Product
        self.product1 = Product.objects.create(
            airplane_id=self.airplane1.id,
            price='100',
            seat_type_id=self.seat_type.id,
            remaining_seat=30,
            total_seats=30,
        )
        self.product2 = Product.objects.create(
            airplane_id=self.airplane2.id,
            price='100',
            seat_type_id=self.seat_type.id,
            remaining_seat=30,
            total_seats=30,
        )
        #Create Reservation
        self.reservation = Reservation.objects.create(user=self.user,head_count=3)
        #Link Reservation and Product
        self.product1.reservation_set.add(self.reservation)
        self.product2.reservation_set.add(self.reservation)

    def tearDown(self):
        User.objects.all().delete()
        Region.objects.all().delete()
        Airline.objects.all().delete()
        SeatType.objects.all().delete()

    def test_post_success(self):
        request = {
            'user': self.user.id,
            'head_count' : 3,
            'product': [self.product1.id, self.product2.id]
        }
        response = self.client.post(self.URL, request, content_type='application/json')
        self.assertEqual(response.status_code,201)

        reservation = Reservation.objects.filter(id=response.json()['id']) 
        self.assertEqual(reservation.exists(),True)

        count = Reservation.objects.prefetch_related('product_set').count()
        self.assertEqual(count, 2)

    def test_post_require_key(self):
        request = {
            'user': self.user.id,
        }
        response = self.client.post(self.URL, request, content_type='application/json')
        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json()['head_count'],['This field is required.'])

    def test_post_does_not_exist_product(self):
        undefined_id = Product.objects.all().last().id+1
        request = {
            'user': self.user.id,
            'head_count' : 3,
            'product': [undefined_id]
        }
        response = self.client.post(self.URL, request, content_type='application/json')
        self.assertEqual(response.status_code,400)

    def test_post_does_not_exist_user(self):
        undefined_id = User.objects.all().last().id+1
        request = {
            'user': undefined_id,
            'head_count' : 3,
            'product': [self.product1.id, self.product2.id]
        }
        response = self.client.post(self.URL, request, content_type='application/json')
        self.assertEqual(response.status_code,400)

    def test_get_succese_code(self):
        response = self.client.get(self.URL, content_type='application/json')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json()['data'][0]['product'][0]['airplane']['from_region']['name'],'군산')
