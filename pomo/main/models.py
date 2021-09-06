from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Item(models.Model):

    title = models.CharField(max_length=50)
    year = models.CharField(max_length=20)


    def __str__(self):
        return self.title




class User(AbstractUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    item = models.ManyToManyField(Item)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.





