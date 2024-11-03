from rest_framework import serializers
from v1.models import *


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionAPI
        fields = ['name','phone','email','amount','transaction_date']