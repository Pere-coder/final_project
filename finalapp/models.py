from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class profile(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    key_password = models.TextField(max_length=1000,null=True,blank=True)
    
    
class hellman_encrypt(models.Model):
    p = models.IntegerField(null=True,blank=True)
    q = models.IntegerField(null=True,blank=True)
    b = models.IntegerField(null=True,blank=True)
    alice = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    


class saved_keys(models.Model):
    Bob = models.IntegerField(null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    

    
    
