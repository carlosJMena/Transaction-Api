from django.db import models

class User(models.Model):
    name = models.CharField(max_length=60)
    email = models.EmailField(max_length=64)
    age = models.IntegerField()

    def __str__(self):
        return self.name


class Transaction(models.Model):
    OUTFLOW = 'outflow'
    INFLOW = 'inflow'

    TYPE = (
        (OUTFLOW, OUTFLOW),
        (INFLOW, INFLOW),
    )

    reference = models.CharField(max_length=60, unique=True)
    account = models.CharField(max_length=60)
    category = models.CharField(max_length=60)
    date = models.DateField()
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    type = models.CharField(choices=TYPE, max_length=16)
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='transactions')
