from dataclasses import field
import django_filters
from .models import JobModel

class JobListingFilter(django_filters.FilterSet):
      
    class Meta:
         
        model = JobModel
        fields =  {
            'position':   ['icontains'],  
            'job_type':  ['exact'], 
            'work_type': ['exact'], 
            'company__location': ['icontains'],
            'min_experience': ['lte'],
            'max_salary' : ['gte'],
            }
      