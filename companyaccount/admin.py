from django.contrib import admin
from companyaccount.models import *
admin.site.unregister(CompanyProfile)

class Company(admin.ModelAdmin):
    list_display = ('company_name','location','industry')

admin.site.register(CompanyProfile, Company)


