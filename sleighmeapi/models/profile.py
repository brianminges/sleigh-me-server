from django.db import models
from sleighmeapi.models.state import State
from sleighmeapi.models.gift_preference import GiftPreference

class Profile(models.Model):
    likes = models.CharField(max_length=150)
    dislikes = models.CharField(max_length=150)
    gift_preference = models.ForeignKey(GiftPreference, on_delete=models.CASCADE)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=20)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    zip = models.CharField(max_length=15)