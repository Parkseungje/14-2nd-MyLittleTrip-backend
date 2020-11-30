from django.db import models

class Reservation(models.Model):
    user_id    = models.ForeignKey('users.User', on_delete = models.CASCADE)
    created_at = models.DateField()

    class Meta:
        db_table = 'reservations'

class Age(models.Model):
    name     = models.CharField(max_length = 20)
    discount = models.DecimalField(max_digits = 2, decimal_places=1)

    class Meta:
        db_table = 'ages'
