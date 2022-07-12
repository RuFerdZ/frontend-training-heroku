from django.db import models
from apps.users.models import User


class Collection(models.Model):
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_favourite = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Link(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)

    def __str__(self):
        return self.name
