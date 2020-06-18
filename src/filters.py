import django_filters
from .models import *
from django_filters import DateFilter

class BillFilter(django_filters.FilterSet):
    from_date = DateFilter(field_name='date',lookup_expr='gte',label='From Date')
    to_date = DateFilter(field_name='date',lookup_expr='lte',label='To Date')
    class Meta:
        model = Bill
        fields = ('buyer','buyer_gst','buyer_address')