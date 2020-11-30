from django.db import models

class User(models.Model):
    name          = models.CharField(max_length = 10)
    email_address = models.CharField(max_length = 30)
    password      = models.CharField(max_length = 30)
    phone_number  = models.CharField(max_length = 20)
    card_number   = models.CharField(max_length = 30, null = True)

    class Meta:
        db_table = 'users'
