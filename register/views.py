from django.shortcuts import render, redirect ,HttpResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm , UserProfileForm
from django.contrib.auth.models import User
from .models import UserProfile
from django import forms

# function to get user ip
def get_ip(request):
    try:
        x_forward = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forward:
            ip = x_forward.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
    except:
        ip = ""
    return ip
# function to handle register form
def register (request):
    if request.method == "POST":

        form = RegisterForm(request.POST)
        #Hidden form
        profile_form = UserProfileForm(request.POST)

        if form.is_valid() and profile_form.is_valid():

            user = form.save()
            profile = profile_form.save(commit=False)

            profile.user = user

            profile.save()

            return redirect("home")
    else:
       # initialise blank form and ip info
       form = RegisterForm()
       profile_form = UserProfileForm(initial={'ip_address': get_ip(request)})

    #render the page
    return render(request, "register/register.html",{"form": form,"profile_form":profile_form})

# handle logout
def logout_req(request):
    logout(request)
    messages.info(request, "Logged out")
    return redirect("/")

#handle login
def login_req(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        if form.is_valid() :

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            #update user ip
            ip = UserProfile.objects.get(user=user)
            ip.value = get_ip(request)
            ip.save()

            if user is not None:

                login(request,user)
                messages.success(request,"Successfully Logged in")
                return redirect('/')
            else:
                return render(request, "register/login.html", {"form": form})
        else:
            return render(request, "register/login.html", {"form": form})

    form = AuthenticationForm()
    profile_form = UserProfileForm(initial={'ip_address': get_ip(request)})
    return render(request, "register/login.html", {"form": form,"profile_form":profile_form })


