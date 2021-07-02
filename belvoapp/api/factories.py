import factory
from api.models import User, Transaction


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction
