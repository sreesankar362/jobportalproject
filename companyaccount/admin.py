from django.contrib import admin
from companyaccount.models import *

from companyaccount.models import CompanyProfile


class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'user', 'industry']


admin.site.register(CompanyProfile, CompanyProfileAdmin)
