from django.shortcuts import render, redirect
from .models import Profile
from django.contrib import messages

def home(request):
    return render(request, 'home.html', {})

def profile_list(request):
    if request.user.is_authenticated: 
        profile= Profile.objects.exclude(user= request.user)
        return render(request, 'profile_list.html', {"profiles" : profile})
    else:
        messages.success(request,("You must be logged in first ti view profile list"))
        return redirect('home')