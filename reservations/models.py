from django.db import models

class Reservation(models.Model):
    user_id     = models.ForeignKey('users.User', on_delete=models.CASCADE)
    created_at  = models.DateField()
    count       = models.IntegerField()
    total_price = models.IntegerField()
    product     = models.ManyToManyField('products.Product', through='ProductReservation') 
    class Meta:
        db_table = 'reservations'

class ProductReservation(models.Model):
    reservation  = models.ForeignKey('Reservation', on_delete=models.CASCADE)
    product      = models.ForeignKey('products.Product', on_delete=models.CASCADE)
