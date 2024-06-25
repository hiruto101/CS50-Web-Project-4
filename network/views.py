from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post


def index(request):
    post = Post.objects.all().order_by('-date')
    paginator = Paginator(post, 10)
    
    # create a list of pages
    num_pages = [x for x in range(1, paginator.count + 1)]
    
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    #print(f"DEBUG", num_pages)
    return render(request, "network/index.html", {
        "posts":posts,
        "pages": num_pages
    })


def profile(request):
    posts = Post.objects.filter(author = request.user).order_by('-date')
    paginator = Paginator(posts, 10)
    print(f"Debug2", paginator.num_pages)
    # create a list of pages
    if(paginator.num_pages <= 1):
        num_pages = [1]
    else:
        num_pages = [x for x in range(1, paginator.count + 1)]
    
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    return render(request, "network/profile.html", {
        "posts":posts,
        "pages": num_pages
    })


def post(request):
    content = request.POST.get("content")
       
    try: 
        # Create a new Post object
        post = Post()
        post.author = request.user
        post.content = content
        
        # Save the Post
        post.save()
        
        print(f"author: {post.author} and content: {post.content}")
        
        return HttpResponseRedirect(reverse("index"))
    except Exception as error:
        print(f"Error {error}")
        return HttpResponseRedirect(reverse("index"))
    

def edit(request):
    pass


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

