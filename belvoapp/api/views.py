from django.db.models import Case, Count, Sum, When
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Transaction, User
from .serializers import (
    AccountSummarySerializer, TransactionSerializer, UserSerializer)


class UserViewSet(
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = User.objects.all().order_by('name')
    serializer_class = UserSerializer

    @action(detail=True, methods=['GET'], url_path='account-summary')
    def account_summary(self, request, pk):
        user = self.get_object()
        date_from = request.query_params.get('date_from', None)
        date_to = request.query_params.get('date_to', None)
        query_params = dict()
        if date_to and date_from:
            query_params['date__range'] = (date_from, date_to)
        queryset = Transaction.objects.filter(
            user_id=user,
            **query_params
        ).values('account').annotate(
            total_inflow=Sum(Case(When(type=Transaction.INFLOW, then='amount'))),
            total_outflow=Sum(Case(When(type=Transaction.OUTFLOW, then='amount'))),
            balance=Sum('amount')
        )
        serializer = AccountSummarySerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'], url_path='category-summary')
    def category_summary(self, request, pk):
        user = self.get_object()
        transactions = Transaction.objects.filter(user_id=user).values(
            'category', 'type').annotate(
            categories=Count('category'),
            inflow=Sum(Case(When(type=Transaction.INFLOW, then='amount'))),
            outflow=Sum(Case(When(type=Transaction.OUTFLOW, then='amount')))
        )
        inflow, outflow = self.category_summary_build_response(transactions)
        return Response({'inflow': inflow, 'outflow': outflow})

    def category_summary_build_response(self, transactions):
        outflow = dict()
        inflow = dict()
        for transaction in transactions:
            category = transaction.get('category')
            inflow_amount = transaction.get('inflow')
            outflow_amount = transaction.get('outflow')
            if transaction.get('type') == Transaction.INFLOW:
                inflow.update({f"{category}": f"{round(inflow_amount, 2)}"})
            else:
                outflow.update({f"{category}": f"{round(outflow_amount, 2)}"})
        return inflow, outflow


class TransactionApiViewSet(CreateModelMixin, GenericViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_serializer(self, *args, **kwargs):
        if 'data' in kwargs:
            data = kwargs['data']

            # check if many is required
            if isinstance(data, list):
                kwargs['many'] = True

        return super(
            TransactionApiViewSet, self).get_serializer(*args, **kwargs)



