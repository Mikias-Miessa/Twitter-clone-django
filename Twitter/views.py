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
        messages.success(request,("You must be logged in first to view profile list"))
        return redirect('home')
def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id = pk)
        if request.method == "POST":
            current_user_profile = request.user.profile
            action = request.POST['follow']
            if action == "follow":
                current_user_profile.follows.add(profile)
            else:
                current_user_profile.follows.remove(profile)
            current_user_profile.save()    
        return render(request,'profile.html',{'profile':profile})
    else:
        messages.success(request,('You must be logged in first'))
        return redirect('home')