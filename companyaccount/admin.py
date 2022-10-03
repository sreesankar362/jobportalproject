from django.contrib import admin
from companyaccount.models import *

# Register your models here.
admin.site.unregister(CompanyProfile)
admin.site.register(CompanyProfile)
admin.site.unregister(SocialProfile)
admin.site.register(SocialProfile)

