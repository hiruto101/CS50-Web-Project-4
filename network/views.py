from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Count
import json

from .models import User, Post, Like


def index(request):
    posts = Post.objects.all().order_by('-date').annotate(lcount=Count('likes'))
    like_list = Like.objects.all()
    paginator = Paginator(posts, 10)
    user_liked = []
    try:
        print("this like", posts[0].like_count())
    except:
        print("none")
            
    try:
        for like in like_list:
            if like.user.id == request.user.id:
                user_liked.append(like.post.id)
    except:
        user_liked = []
        
        
    page_number = request.GET.get('page')
    postinator = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "posts":postinator,
        "likelists":user_liked
    })


def profile(request):
    posts = Post.objects.filter(author = request.user).order_by('-date')
    paginator = Paginator(posts, 10)
    
    
    # create a list of pages
    
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    return render(request, "network/profile.html", {
        "posts":posts,
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
    

def edit(request, post_id):
    if request.method == "POST":
        raw_data = request.body
        data = json.loads(raw_data)
        
        print(data['content'], post_id)
    return JsonResponse({"message": "Edited"})

# Set Like or Unlike
def like(request, post_id):
    if request.method == "POST":
        
        data = json.loads(request.body)
        post = Post.objects.get(pk=post_id)
        user = User.objects.get(pk = request.user.id)
        n_like = ""
        
        try:
            like_user = User.objects.get(id = request.user.id)
            like_post = Post.objects.get(id = post_id)
        except User.DoesNotExist:
            print("User does not exist")
        except Post.DoesNotExist:
            print("Post does not exist")
            
        like = Like(user=like_user, post=like_post)
        
        if data["stat"] == "like":
            try:
                like.save()
                post.likes.add(user)
                n_like = Like.objects.filter(post = post).count()
                print("Liked ", n_like)
                return JsonResponse({"message": "liked",
                                     "likes": n_like})
            except Exception as e:
                print(f"Error: {e}")
                return JsonResponse({"Error": "Already Liked"})
        else:
            try:
                unlike = Like.objects.filter(user=like_user, post = like_post)
                unlike.delete()
                post.likes.remove(user)
                n_like = Like.objects.filter(post = post).count()
                print("Unlike: ", n_like)
                return JsonResponse({"message": "unlike",
                                     "likes": n_like})
            except Exception as e:
                print(f"Error: {e}")
                return JsonResponse({"Error": "Delete Error"})
    #GET
    return JsonResponse({"message": "GET"})


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

