from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    accessToken = models.TextField(blank=True)
    refreshToken = models.TextField(blank=True)
    tokenMaxTime = models.IntegerField(default=3600)
    tokenRequestTime = models.DateTimeField(blank=True)
    profilePic = models.TextField(blank=True)
    lastPlaylist = models.TextField(blank=True)