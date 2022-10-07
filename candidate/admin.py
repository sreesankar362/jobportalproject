from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(CandidateProfile)

admin.site.register(LatEducation)

admin.site.register(Experience)

admin.site.register(Skill)