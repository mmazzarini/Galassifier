from django.db import models

# Create your models here.

from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # additional properties
    number_galaxies_classified = models.IntegerField(default=0)
    number_ellipticals = models.IntegerField(default=0)
    number_spirals = models.IntegerField(default=0)
    number_uncertain = models.IntegerField(default=0)
    user_credits = models.IntegerField(default=0)
    user_country = models.TextField(default="UK")


class GalaxyInformation(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.TextField(default="None")
    galaxyType = models.TextField(default="None")
    related_name="galaxies"
