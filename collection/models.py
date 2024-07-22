import uuid

from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    genres = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.title} - {self.uuid}'


class Collection(models.Model):
    title = models.CharField(max_length=100)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="collections")
    movies = models.ManyToManyField(Movie, related_name='collections')

    def __str__(self):
        return self.title
