from django.contrib import admin
from companyaccount.models import *

# Register your models here.
admin.site.unregister(CompanyProfile)
# admin.site.unregister(SocialProfile)
# admin.site.register(SocialProfile)

class Company(admin.ModelAdmin):
    list_display = ('company_name','location','industry')

admin.site.register(CompanyProfile, Company)