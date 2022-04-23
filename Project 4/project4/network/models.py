from time import time
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField('self', related_name='followers', blank=True, null=True)


class Post(models.Model):
    content = models.TextField(max_length=255, verbose_name='post_content')
    likes = models.IntegerField(default=0)
    date_published = models.DateTimeField(auto_now_add=True)
    poster = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)