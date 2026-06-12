from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Society Admin'),
        ('RESIDENT', 'Resident'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='RESIDENT')

    def is_admin_role(self):
        return self.role == 'ADMIN'

    def is_resident_role(self):
        return self.role == 'RESIDENT'

