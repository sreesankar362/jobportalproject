from django.contrib import admin

from companyaccount.models import Company

# Register your models here.




class CompanyAdmin(admin.ModelAdmin):
    exclude = ('social_profile',)


admin.site.register(Company,CompanyAdmin)
