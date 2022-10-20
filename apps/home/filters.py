from dataclasses import field
import django_filters
from .models import JobModel

class JobListingFilter(django_filters.FilterSet):
    position = django_filters.CharFilter(lookup_expr='gte', label='Position')
    # job_type = django_filters.CharFilter(lookup_expr= 'exact')
    # work_type= django_filters.CharFilter(lookup_expr= 'exact')
    # company__location = django_filters.CharFilter(lookup_expr='icontains', label='Location')
    # max_salary = django_filters.CharFilter(lookup_expr='gte', label='Salary')
    min_experience =django_filters.CharFilter(lookup_expr='lte', label='Experience')
    class Meta:
        model = JobModel
        

        
        fields = ['position', 'min_experience', 'work_type', 'job_type']
