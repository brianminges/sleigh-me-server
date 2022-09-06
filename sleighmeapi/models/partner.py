from django.db import models
from sleighmeapi.models.group import Group
from sleighmeapi.models.member import Member

class Partner(models.Model):
    giver = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="giving_partner")
    receiver = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="receiving_partner")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="partners")