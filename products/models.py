from django.db import models

class Product(models.Model):
    airplane        = models.ForeignKey('Airplane', on_delete=models.CASCADE)
    price           = models.DecimalField(max_digits=15, decimal_places=2)
    seat_type       = models.ForeignKey('SeatType', on_delete=models.CASCADE)
    remaining_seat  = models.IntegerField()
    total_seats     = models.IntegerField()

    class Meta:
        db_table = 'products'

class Airplane(models.Model):
    airline           = models.ForeignKey('Airline', on_delete=models.CASCADE)
    from_region       = models.ForeignKey('Region', on_delete=models.CASCADE, related_name='departure_region')
    to_region         = models.ForeignKey('Region', on_delete=models.CASCADE, related_name='arrival_region')
    from_date         = models.DateTimeField()
    to_date           = models.DateTimeField()
    airplane_numbers  = models.CharField(max_length=15)

    class Meta:
        db_table = 'airplanes'

class SeatType(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'seat_types'

class Airline(models.Model):
    name      = models.CharField(max_length=30)
    image_url = models.CharField(max_length=100)

    class Meta:
        db_table = 'airlines'

class Region(models.Model):
    name         = models.CharField(max_length=20)
    region_code  = models.CharField(max_length=10)
    image_url    = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'regions'
