from django.shortcuts import render, redirect,get_object_or_404
from .models import Profile, Tweets
from django.contrib import messages
from .forms import TweetForm, SignUpForm,ProfilePictureForm,TweetPictureForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def tweet(request):
    if request.user.is_authenticated:
        # pic_form = TweetPictureForm(request.POST or None, request.FILES or None)
        form = TweetForm(request.POST or None, request.FILES or None)
        if request.method == "POST":
            if form.is_valid() :
                tweet= form.save(commit= False)
                # pic = pic_form.save( commit=False)
                tweet.user = request.user
                # pic.user = request.user
                tweet.save()
                # pic.save()
                messages.success(request, "Your tweet is posted!")
                return redirect('home')
        else:
            return render(request, 'tweet.html' , {'form':form})
    else:
        messages.success(request,'You must be logged in to tweet!')
        return redirect('home')

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
        # current_user_profile = Profile.objects.get(user__id = request.user.id)
        # following = current_user_profile.follows.all()
        tweets = Tweets.objects.all().order_by("-created_at")
        # following_tweets = Tweets.objects.filter(user__in= current_user_profile.follows.all() ).order_by("-created_at")
        
        return render(request, 'home.html', {"tweets":tweets,"form":form})
    else:
        #  tweets = Tweets.objects.all().order_by("-created_at")
         messages.success(request,"You must login first!")
         return redirect('login')

def profile_list(request):
    if request.user.is_authenticated: 
        profile= Profile.objects.exclude(user= request.user)
        
        return render(request, 'profile_list.html', {"profiles" : profile})
    else:
        messages.success(request,("You must be logged in first to view profile list"))
        return redirect('login')
def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id = pk)
        tweets= Tweets.objects.filter(user_id = pk).order_by("-created_at")
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
        return redirect('login')


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
    return redirect('login')

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

def edit_profile(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id= request.user.id)
        current_user_profile = Profile.objects.get(user__id = request.user.id)
        form = SignUpForm(request.POST or None, request.FILES or None, instance = current_user)
        pic_form = ProfilePictureForm(request.POST or None, request.FILES or None, instance=current_user_profile)
        if request.method == 'POST':
            if form.is_valid() and pic_form.is_valid():
                form.save()
                pic_form.save()
                login(request, current_user)
                messages.success(request,('Your profile is updated!'))
                return redirect('home')
        else:    
            return render(request, 'edit_profile.html',{'form':form, 'pic_form':pic_form})
    else:
        messages.success(request,('you must be logged in to edit a profile'))
        return redirect('login')

def like_tweet(request, pk):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweets , id= pk )
        # if tweet.likes.filter(id = request.user.id):
        if request.user in tweet.likes.all():
            tweet.likes.remove(request.user)
        else:
            tweet.likes.add(request.user)
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request,('you must be logged in'))
        return redirect('login')