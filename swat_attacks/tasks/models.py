from django.db import models

class Post(models.Model):
    target = models.CharField(max_length=100)
    attack_type = models.DecimalField()
    state = models.DecimalField()
    owner = models.CharField(max_length=100)

    def __str__(self):
        return self.title

