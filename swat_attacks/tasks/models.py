from djongo import models
from bson import ObjectId

class Attack(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId, editable=False)
    target = models.CharField(max_length=100)
    attack_type = models.JSONField()
    state = models.CharField(max_length=20)
    owner = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.target

class Generic_Result(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId, editable=False)
    vulnerable_urls = models.JSONField()
    payloads = models.JSONField()
    level = models.CharField(max_length=20)
    attack_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
