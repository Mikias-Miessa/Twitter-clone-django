from django.shortcuts import render, redirect
from .models import Profile, Tweets
from django.contrib import messages
from .forms import TweetForm, SignUpForm
from django.contrib.auth import authenticate, login, logout

def home(request):
    if request.user.is_authenticated:
        form= TweetForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid:
                tweet= form.save(commit= False)
                tweet.user = request.user
                tweet.save()
                messages.success(request, "Your tweet is posted!")
                return redirect('home')
        tweets = Tweets.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"tweets":tweets,"form":form})
    else:
         tweets = Tweets.objects.all().order_by("-created_at")
         return render(request, 'home.html', {"tweets":tweets})

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
        tweets= Tweets.objects.filter(user_id = pk)
        current_user_profile = request.user.profile
        if request.method == "POST":
            
            action = request.POST['follow']
            if action == "follow":
                current_user_profile.follows.add(profile)
            else:
                current_user_profile.follows.remove(profile)
            current_user_profile.save()    
        return render(request,'profile.html',{'profile':profile, "tweets":tweets, "current_user":current_user_profile})
    else:
        messages.success(request,('You must be logged in first'))
        return redirect('home')


def login_user(request):
    if request.method== 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user= authenticate(request, username= username, password= password)
        if user is not None:
            login(request, user)
            messages.success(request,('Login successful!'))
            return redirect('home')
        else:
            messages.success(request,('Try again please'))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request,('You have logged out!'))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method== 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username = username, password= password)
            login(request,user)
            messages.success(request,('Wellcome to Twitter!'))
            return redirect('home')
    
    return render(request, 'register.html',{'form':form})

# def register_user(request):
# 	form = SignUpForm()
# 	if request.method == "POST":
# 		form = SignUpForm(request.POST)
# 		if form.is_valid():
# 			form.save()
# 			username = form.cleaned_data['username']
# 			password = form.cleaned_data['password1']
# 			# first_name = form.cleaned_data['first_name']
# 			# second_name = form.cleaned_data['second_name']
# 			# email = form.cleaned_data['email']
# 			# Log in user
# 			user = authenticate(username=username, password=password)
# 			login(request,user)
# 			messages.success(request, ("You have successfully registered! Welcome!"))
# 			return redirect('home')
	
# 	return render(request, "register.html", {'form':form})