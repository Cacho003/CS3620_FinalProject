from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Profile
from .forms import PostForm, RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth import logout as auth_logout

# Create your views here.
@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'myapp/create_post.html', {'form': form})

@login_required
def home(request):
    profile = request.user.profile
    friends = profile.friends.all()
    posts = Post.objects.filter(user__profile__in=friends).order_by('-created_at')
    if not posts.exists():
        no_posts = True
    else:
        no_posts = False

    return render(request, 'myapp/home.html', {'posts': posts, 'no_posts': no_posts})

def post(request, slug):
    post = Post.objects.get(slug=slug)
    return render(request, 'myapp/create_post.html', {'post': post})

def profile(request):
    friends = request.user.profile.friends.all()
    return render(request, 'myapp/profile.html')

@login_required
def user_list(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'myapp/user_list.html', {'users': users})

@login_required
def add_friend(request, user_id):
    friend_user = get_object_or_404(User, id=user_id)
    friend_profile = get_object_or_404(Profile, user=friend_user)
    request.user.profile.friends.add(friend_profile)
    return redirect('profile_view')

def profile_view(request):
    friends = request.user.profile.friends.all()
    return render(request, 'myapp/profile.html', {'friends': friends})

@login_required
def remove_friend(request, user_id):
    friend = get_object_or_404(User, id=user_id)
    request.user.profile.friends.remove(friend.profile)
    return redirect('profile')

@login_required
def logout(request):
    auth_logout(request)
    return redirect('login')

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'myapp/register.html', {'form': form})
