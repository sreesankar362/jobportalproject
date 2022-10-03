from django.shortcuts import render,redirect
from django.views.generic import View,TemplateView
from user.models import ApplicantUser
from user import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

class RegistrationView(View):
    def get(self,request,*args,**kwargs):
        form = forms.RegistrationForm()
        return render(request,"registration.html",context={"form":form})
    def post(self,request,*args,**kwargs):
        print(request.POST.get("username"))
        print(request.POST.get("password"))
        form = forms.RegistrationForm(request.POST,request.FILES)
        if form.is_valid():
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            password = request.POST['password']
            email = request.POST['email']
            mobile = request.POST['mobile']
            gender = request.POST['gender']
            profile_pic = request.FILES['profile_pic']
            #is_mail_verified = request.POST['is_mail_verified']
            dob = request.POST['dob']
            #is_phone_verified = request.POST['is_phone_verified']
            bio = request.POST['bio']
            location = request.POST['location']
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password, email=email)
            applicant = ApplicantUser.objects.create(user=user,mobile=mobile,bio=bio,location=location,
                                                     gender=gender,dob=dob,profile_pic=profile_pic)


            return redirect("home")
        else:
            print("Error..................................")
            return render("home.html")

        return render(request, "login.html")



class LogInView(View):
    def get(self,request,*args,**kwargs):
        form = forms.LoginForm()
        return render(request,"login.html",context={"form":form})
    def post(self,request,*args,**kwargs):
        form =forms.LoginForm(request.POST)
        if form.is_valid():
            username= form.cleaned_data.get("username")
            password= form.cleaned_data.get("password")
            user = authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                print("success")
                return redirect("welcome")
            else:
                print("failure")
                return render(request,"login.html",context={"form":form})
        return render(request,"registration.html")


class LogOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        print("loggged out Successfully")
        return redirect("home")

class WelcomeView(TemplateView):
    def get(self,request,*args,**kwargs):
        user = ApplicantUser.objects.get(user=request.user)
        print(user.profile_pic.url)
        return render(request,"welcome.html",context={"user":user})
