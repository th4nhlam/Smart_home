from django.db import models

# Create your models here.
class Device(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    type = models.CharField(max_length=60)
    status = models.CharField(max_length=60)