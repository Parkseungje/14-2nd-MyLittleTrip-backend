from django.db import models

class Reservation(models.Model):
    user        = models.ForeignKey('users.User', on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)
    head_count  = models.IntegerField()
    product     = models.ManyToManyField('products.Product')

    class Meta:
        db_table = 'reservations'

