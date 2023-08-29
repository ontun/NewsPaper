from django_filters import FilterSet, ChoiceFilter, DateTimeFilter, DateRangeFilter, DateFilter
from .models import Post, Category
from django import forms

class NewsFilter(FilterSet):
   category = ChoiceFilter(choices=Category.objects.values_list('id', 'category_name'), label='Category')
   post_dt = DateFilter(field_name='post_dt', widget=forms.TextInput(attrs={'type': 'date'}), label='Date', lookup_expr='gte')
   class Meta:
       model = Post
       fields = {
           # поиск по названию
           'post_tittle': ['icontains'],
           #
       }