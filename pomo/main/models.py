from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Item(models.Model):

    title = models.CharField(max_length=50)
    year = models.CharField(max_length=20)
    genre = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.title


class Myuser(models.Model):
    email = models.EmailField(unique=True)
    item = models.ManyToManyField(Item)
    
    

    def __str__(self):
        return self.email