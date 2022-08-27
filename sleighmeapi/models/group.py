from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=50)
    creator = models.ForeignKey("sleighmeapi.Member", on_delete=models.CASCADE)
    guidelines = models.CharField(max_length=150)
    date = models.DateField()
    time = models.TimeField()