from django.db import models
from django.contrib.auth.models import User

class Monitoring(models.Model):
    STATUS_CHOICES = (
        ("income", "Kirim"),
        ("expense", "Chiqim")
    )

    TYPE_CHOICES = (
        ("card", "Karta"),
        ("cash", "Naqt")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    created_at = models.DateTimeField(auto_now_add=True)
    payment_type = models.CharField(choices=TYPE_CHOICES, max_length=10)
    status = models.CharField(choices=STATUS_CHOICES, max_length=10)  
    price = models.DecimalField(max_digits=10, decimal_places=0)  
    comment = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'monitoring' 

