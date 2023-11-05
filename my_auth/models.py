from django.db import models

from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True, blank=True)
    email = models.EmailField(max_length=100, blank=False) # mandatory fields
    password = models.CharField(max_length=100, blank=False) # mandatory fields
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)

    