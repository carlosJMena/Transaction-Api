from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Transaction, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class BulkCreateTransactionListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        objs = [Transaction(**data) for data in validated_data]
        return Transaction.objects.bulk_create(objs, ignore_conflicts=True)


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        list_serializer_class = BulkCreateTransactionListSerializer

    def validate(self, attrs):
        reference = attrs['reference']
        amount = attrs['amount']
        type = attrs['type']
        if amount > 0 and not type == Transaction.INFLOW or amount < 0 \
                and not type == Transaction.OUTFLOW:
            raise ValidationError(
                {"type": f'Wrong transaction type with reference: {reference}'}
            )
        return attrs

    def validate_amount(self, amount):
        if amount == 0:
            raise ValidationError('cannot be zero')
        return amount


class AccountSummarySerializer(serializers.Serializer):
    account = serializers.CharField()
    balance = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_inflow = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_outflow = serializers.DecimalField(max_digits=15, decimal_places=2)
