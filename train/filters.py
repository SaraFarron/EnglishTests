from django_filters import CharFilter
import django_filters
from .models import *


class WordFilter(django_filters.FilterSet):
    english = CharFilter(field_name='english', lookup_expr='icontains')


    class Meta:
        model = Word
        fields = '__all__'
        exclude = [
            'times_learned',
            'is_learned'
        ]
