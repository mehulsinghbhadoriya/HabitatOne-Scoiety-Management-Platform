from django.db import models
from django.conf import settings

class Resident(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resident_profile')
    flat_number = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    family_members = models.PositiveIntegerField(default=1)
    move_in_date = models.DateField()

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.flat_number}"

