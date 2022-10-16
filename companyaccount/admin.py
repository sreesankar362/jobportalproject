from django.contrib import admin
from companyaccount.models import *
from django.utils.html import format_html
from companyaccount.models import CompanyProfile

admin.site.site_header = "JOBHUB ADMIN"
admin.site.site_title = "JOBHUB"
admin.site.index_title = "JOBHUB"


class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'image_tag', 'user', 'is_approved', 'industry']
    list_filter = ['is_approved']
    readonly_fields = [
                       'company_name', 'user', 'company_logo', 'industry',
                       'company_description', 'location', 'category', 'team_size',
                       'founded', 'company_address', 'is_activated'
                       ]
    search_fields = ('company_name', 'company_description')

    def image_tag(self, obj):
        return format_html('<img src="{}" width="100px" height="100px" />'.format(obj.company_logo.url))

    image_tag.short_description = 'Logo'


admin.site.register(CompanyProfile, CompanyProfileAdmin)
