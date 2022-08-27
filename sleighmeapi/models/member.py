from django.db import models
from django.contrib.auth.models import User
from sleighmeapi.models.group import Group
from sleighmeapi.models.profile import Profile

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="member")
    groups = models.ManyToManyField(Group, related_name="members")