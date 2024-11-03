from django.db import models
from django.utils import timezone
import uuid
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class TransactionAPI(models.Model):
    STATUS = [
        ('Pending','Pending'),
        ('Approved','Approved'),
        ('Rejected','Rejected'),
    ]

    transaction_id = models.CharField(max_length=20, unique=True, editable=False)
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateField()
    status = models.CharField(max_length=20,choices=STATUS, default='Pending')


    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = self.generate_id()
        return super().save(*args, **kwargs)
    
    def generate_id(self):
        unique_id = str(uuid.uuid4().int)[:6]
        return f'TXNID{unique_id.zfill(6)}'
    

    def __str__(self):
        return self.transaction_id