from django.db import models
from django.contrib.auth.models import User
from django.db.models.lookups import IRegex
from django.forms.models import ModelForm


# Create your models here.
class Item(models.Model):

    title = models.CharField(max_length=50)
    year = models.CharField(max_length=20)
    genre = models.CharField(max_length=100,null=True)
    released = models.CharField(max_length=100,null=True)
    runtime = models.CharField(max_length=100,null=True)
    cast = models.CharField(max_length=200,null=True)
    plot = models.TextField(null=True)
    country = models.CharField(max_length=100,null=True)
    poster_link = models.CharField(max_length=2048,null=True)
    metascore = models.CharField(max_length=100,null=True)
    imdbRating = models.CharField(max_length=100,null=True)
    type = models.CharField(max_length=20,null=True)
    imdb_id = models.CharField(max_length=100,null=True)

    liked = models.ManyToManyField(User, default=None, blank=True,related_name='liked')



    def __str__(self):
        return self.title

    @property
    def num_likes(self):
        return self.liked.all().count()





LIKE_CHOICES = (
    ('Like','Like'),
    ('Unlike','Unlike'),
)



class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES,default='Like',max_length=10)


    def __str__(self):
        return str(self.item)







class Myuser(models.Model):
    email = models.EmailField(unique=True)
    item = models.ManyToManyField(Item)
    username= models.CharField(max_length=100,null=True)

    watched = models.ManyToManyField(Item,related_name='watched')
    
    

    def __str__(self):
        return self.email