from django.db import models
from residents.models import Resident

class MaintenanceBill(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
    )
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name='bills')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"Bill for {self.resident.user.get_full_name()} - {self.amount} (Due: {self.due_date})"

