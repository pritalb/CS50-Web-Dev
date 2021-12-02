from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    poster = models.OneToOneField(User, verbose_name=_(""), on_delete=models.CASCADE)
    content = models.CharField(max_length=144)
    likes = None
    date_published = models.DateTimeField(auto_now_add=True)
    comments = None

    class Meta:
        verbose_name = _("")
        verbose_name_plural = _("s")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})

class Comment(models.Model):
    post = None
    user = None