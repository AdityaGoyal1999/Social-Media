from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.CharField(max_length=500)
    pub_time = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    def __str__(self):
        return self.content