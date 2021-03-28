from django.db import models

# Create your models here.

class Location(models.Model): 
    country = models.CharField(max_length=50)
    apisource = models.CharField(max_length=200)
    resourceurl = models.CharField(max_length=200)
    population = models.BigIntegerField()
