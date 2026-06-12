from django.db import models
from residents.models import Resident

class Visitor(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name='visitors')
    visitor_name = models.CharField(max_length=100)
    visit_date = models.DateField()
    purpose = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.visitor_name} visiting Flat {self.resident.flat_number} on {self.visit_date}"

