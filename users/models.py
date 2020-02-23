from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    age = models.IntegerField(default=0)

class SpotifyUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    spotify_email = models.CharField(max_length=100)
    spotify_name = models.CharField(max_length=100)
    spotify_id = models.CharField(max_length=25)
    refresh_token = models.CharField(max_length=200)
