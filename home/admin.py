from django.contrib import admin

from companyaccount.models import CompanyProfile, SocialProfile

# Register your models here

admin.site.register(CompanyProfile)
admin.site.register(SocialProfile)