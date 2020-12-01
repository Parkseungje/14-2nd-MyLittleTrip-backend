from django.db import models

class Reservation(models.Model):
    user_id     = models.ForeignKey('users.User', on_delete = models.CASCADE)
    created_at  = models.DateField()
    count       = models.IntegerField()
    total_price = models.IntegerField()

    class Meta:
        db_table = 'reservations'

