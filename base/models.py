from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)

    # Use email instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Extract(models.Model):
    data = models.CharField(max_length=10000, null=True)

    def __str__(self):
        return self.data


class Upload(models.Model):
    photo = models.ImageField(null=False)


class Nutrition(models.Model):
    food = models.CharField(max_length=1000)

    def __str__(self):
        return self.food