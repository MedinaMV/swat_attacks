from djongo import models
from django import forms
from bson import ObjectId

class Attack(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId, editable=False)
    target = models.CharField(max_length=100)
    attack_type = models.JSONField()
    state = models.CharField(max_length=20)
    owner = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    finished_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.target

class Result(models.Model):
    url = models.CharField(max_length=80)
    payload = models.CharField(max_length=50)
    
    class Meta:
        abstract = True

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ('url', 'payload')
        
class Generic_Result(models.Model): 
    _id = models.ObjectIdField(primary_key=True, default=ObjectId, editable=False)
    name = models.CharField(max_length=10)
    results = models.ArrayField(
        model_container=Result,
        model_form_class=ResultForm
    )
    level = models.CharField(max_length=20)
    attack_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    objects = models.DjongoManager()


class Bruteforce_Result(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId, editable=False)
    vulnerable_ddos = models.BooleanField()
    username = models.CharField(max_length=80)
    password = models.CharField(max_length=50)
    level = models.CharField(max_length=20)
    attack_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.DjongoManager()

class Nuclei(models.Model):
    vulnerability = models.CharField(max_length=100)
    
    class Meta:
        abstract = True
    
class NucleiForm(forms.ModelForm):
    class Meta:
        model = Nuclei
        fields = ('vulnerability',)

class Nuclei_Result(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId, editable=False)
    results = models.ArrayField(
        model_container=Nuclei,
        model_form_class=NucleiForm
    )
    attack_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.DjongoManager()