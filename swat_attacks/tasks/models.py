from django.db import models

# Create your models here.
class task(models.Model):
    type = models.CharField(max_length=4)
    done = models.CharField(max_length=1)
