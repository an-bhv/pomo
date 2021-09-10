from django.contrib import admin
from .models import Myuser,Item,Like,Comment

# Register your models here.

admin.site.register(Item)
admin.site.register(Myuser)
admin.site.register(Like)
admin.site.register(Comment)
