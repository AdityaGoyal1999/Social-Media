from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post, Follow


# The main page that contains all the posts
def index(request):

    posts = Post.objects.all()

    posts = list(reversed(posts))

    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    posts = paginator.get_page(1)
    context = {"posts": posts}

    return render(request, "network/index.html", context=context)


# Present the login page
def login_view(request):

    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            # Keep track of username
            request.session['username'] = username
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


# Log the user out
def logout_view(request):

    logout(request)
    request.session.flush()
    return HttpResponseRedirect(reverse("index"))


# Shows the profile page of a given user
def profile(request, name):

    curr_user = User.objects.filter(username=request.session['username']).first()
    user = User.objects.filter(username=name).first()

    followers = Follow.objects.filter(followee=user)
    follows = Follow.objects.filter(follower=user)
    
    follow_connection = Follow.objects.filter(follower=curr_user, followee=user).first()
    if follow_connection is None:
        following = False
    else:
        following = True

    posts = Post.objects.filter(publisher=user)
    return render(request, "network/profile_page.html", {"followers": followers, "followings": follows, "posts": posts, "curr_user": user, "following": following,})


# Register a new user
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


# Shows the posts of the users following
def following(request):

    user = User.objects.filter(username=request.session['username']).first()
    follows = Follow.objects.filter(follower=user)
    posts = Post.objects.all()

    users_follows = []
    for follow in follows:
        users_follows.append(follow.followee)

    follows_posts_list = []
    for p in posts:
        if p.publisher in users_follows:
            follows_posts_list.append(p)

    all_users = User.objects.all()

    return render(request, "network/following.html", {"posts": follows_posts_list, "users": all_users,})


# Create a new post
def create_post(request):

    content = request.POST['content']

    user = User.objects.filter(username=request.session['username']).first()
    post = Post.objects.create(content=content, publisher=user)

    return HttpResponseRedirect(reverse("index"))


# Designed for the paginator class for Django
def listing(request, page_number):

    posts = Post.objects.all()
    paginator = Paginator(posts, 10) # Show 10 posts per page

    posts = paginator.get_page(page_number)

    return render(request, "network/index.html", {"posts":posts,})


# Edit a post
def edit_post(request, pk, content):

    post = Post.objects.get(pk=pk)

    # Securing the editing process
    if post.publisher.username == request.session['username']:
        post.content = content
        post.save()
    else:
        raise Http404("Cannot edit someone else's post")

    return HttpResponse(post.content)


# Like a post
def like(request, pk):

    post = Post.objects.get(pk=pk)
    post.likes += 1
    post.save()

    return HttpResponse("Edited")


# Follow a given user
def follow(request, name):
    
    follower = User.objects.filter(username=request.session['username']).first()
    followee = User.objects.filter(username=name).first()

    follow = Follow.objects.create(follower=follower, followee=followee)

    follows = Follow.objects.filter(follower=follower)

    users_follows = []
    for follow in follows:
        users_follows.append(follow.followee)

    posts = Post.objects.all()

    follows_posts_list = []
    for p in posts:
        if p.publisher in users_follows:
            follows_posts_list.append(p)

    all_users = User.objects.all()

    return render(request, "network/following.html", {"posts": follows_posts_list, "users": all_users, "message": "Following the user.",})


# Unfollow a given user
def unfollow(request, name):
    
    follower = User.objects.filter(username=request.session['username']).first()
    followee = User.objects.filter(username=name).first()

    delete_follow = Follow.objects.filter(follower=follower, followee=followee).delete()
    follows = Follow.objects.filter(follower=follower)

    users_follows = []
    for follow in follows:
        users_follows.append(follow.followee)

    posts = Post.objects.all()

    follows_posts_list = []
    for p in posts:
        if p.publisher in users_follows:
            follows_posts_list.append(p)

    all_users = User.objects.all()

    return render(request, "network/following.html", {"posts": follows_posts_list, "users": all_users, "message": "Unfollowed the user.",})