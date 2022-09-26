from django.shortcuts import render
from django.views.generic import View


class HomeView(View):
    def get(self,request):
        return render(request,"home.html")


class JobListingView(View):
    def get(self,request):
        return render(request,"job_listing.html")
