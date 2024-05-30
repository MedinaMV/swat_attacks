from djongo import models
from django.core.exceptions import ValidationError
from bson import ObjectId

def validate_single_digit(value):
    if value < 0 or value > 9:
        raise ValidationError(
            '%(value)s no es un número de una sola cifra',
            params={'value': value},
        )

class Attack(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId, editable=False)
    target = models.CharField(max_length=100)
    attack_type = models.IntegerField()
    state = models.IntegerField()
    owner = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.target
