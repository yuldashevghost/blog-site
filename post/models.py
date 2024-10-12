from datetime import timezone

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.
# myapp/models.py

from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class Post(models.Model):
    cover_image = models.ImageField(upload_to="posts/%Y/%m/%d/")
    title = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
