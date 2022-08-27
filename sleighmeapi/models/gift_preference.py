from django.db import models

class GiftPreference(models.Model):
    option = models.CharField(max_length=50)
    