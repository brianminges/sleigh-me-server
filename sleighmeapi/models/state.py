from django.db import models

class State(models.Model):
    name = models.CharField(max_length=15)
    abbreviation = models.CharField(max_length=2)