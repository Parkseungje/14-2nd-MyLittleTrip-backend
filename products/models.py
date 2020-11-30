from django.db import models

class Product(models.Model):
    airplane_id    = models.ForeignKey('Airplane', on_delete = models.CASCADE)
    price          = models.IntegerField()
    seat_type_id   = models.ForeignKey('SeatType', on_delete = models.CASCADE)
    remaining_seat = models.IntegerField()
    tatal_seat     = models.IntegerField()

    class Meta:
        db_table = 'products'

class Airplane(models.Model):
    airline        = models.ForeignKey('Airline', on_delete = models.CASCADE)
    from_region_id = models.ForeignKey('Region', on_delete  = models.CASCADE, related_name='from_region_id')
    to_region_id   = models.ForeignKey('Region', on_delete  = models.CASCADE, related_name='to_region_id')
    from_time      = models.TimeField()
    to_time        = models.TimeField()
    from_date      = models.DateField()
    to_date        = models.DateField()

    class Meta:
        db_table = 'airplanes'

class SeatType(models.Model):
    name = models.CharField(max_length = 20)

    class Meta:
        db_table = 'seatypes'

class Airline(models.Model):
    name      = models.CharField(max_length = 30)
    image_url = models.CharField(max_length = 100)

    class Meta:
        db_table = 'airlines'

class Reservation_age(models.Model):
    reservation_id = models.ForeignKey('reservations.Reservation', on_delete = models.CASCADE)
    age_id         = models.ForeignKey('reservations.Age', on_delete         = models.CASCADE)
    count          = models.IntegerField()

    class Meta:
        db_table = 'reservation_ages'

class Product_reservation(models.Model):
    reservation_id = models.ForeignKey('reservations.Reservation', on_delete = models.CASCADE)
    product_id     = models.ForeignKey('Product', on_delete                  = models.CASCADE)
    total_price    = models.IntegerField()

    class Meta:
        db_table = 'product_reservations'

class Region(models.Model):
    name      = models.CharField(max_length = 20)
    initial   = models.CharField(max_length = 10)
    image_url = models.CharField(max_length = 100, null = True)

    class Meta:
        db_table = 'Regions'
