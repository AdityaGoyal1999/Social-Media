from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post, Follow


def index(request):

    # TODO: reverse the list
    posts = Post.objects.all()
    # Reverses the list according to the most recent posts
    posts = list(reversed(posts))

    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    posts = paginator.get_page(1)
    context = {"posts": posts}

    return render(request, "network/index.html", context=context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            request.session['username'] = username
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    request.session.flush()
    return HttpResponseRedirect(reverse("index"))

def profile(request, name):

    user = User.objects.filter(username=name).first()

    followers = Follow.objects.filter(followee=user)
    follows = Follow.objects.filter(follower=user)

    posts = Post.objects.filter(publisher=user)
    return render(request, "network/profile_page.html", {"followers": followers, "followings": follows, "posts": posts})


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        request.session['username'] = username
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def following(request):

    user = User.objects.filter(username=request.session['username']).first()
    follows = Follow.objects.filter(follower=user)
    posts = Post.objects.all()

    follows_posts_list = []
    for p in posts:
        if p.publisher in follows:
            follows_posts_list.append(p)

    return render(request, "network/following.html", {"posts": follows_posts_list,})

def create_post(request):
    content = request.POST['content']

    user = User.objects.filter(username=request.session['username']).first()
    post = Post.objects.create(content=content, publisher=user)

    return HttpResponseRedirect(reverse("index"))


def posts(request):
    user = User.objects.filter(username=request.session['username']).first()
    # Should change this with foreign keys
    posts = Post.objects.filter(publisher=user)
    print(posts, "\n\n")
    return HttpResponse("In the shell")

def listing(request, page_number):
    posts = Post.objects.all()
    paginator = Paginator(posts, 10) # Show 10 posts per page

    # page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(request, "network/index.html", {"posts":posts,})

def edit_post(request, pk, content):

    post = Post.objects.get(pk=pk)

    # Securing the editing process
    if post.publisher.username == request.session['username']:
        post.content = content
        post.save()
    else:
        raise Http404("Cannot edit someone else's post")

    return HttpResponse(post.content)