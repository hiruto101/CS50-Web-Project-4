from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Count, Q
import json

from .models import User, Post, Like, Follow


def index(request):
    posts = Post.objects.all().order_by('-date').annotate(lcount=Count('likes'))
    like_list = Like.objects.all()
    paginator = Paginator(posts, 10)
    user_liked = []
  
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

# Profile for other user "not logged in user"
def profile(request, id):
    is_following = False
    
    get_id = Post.objects.get(pk=id) # id is post ID
    
    # get the Profile User object
    get_user = User.objects.get(username = get_id.author)
    get_userId = get_user.pk
    nam = str(get_user.username)
    # TODO if the currently logged in user views a profile that he follow show unfollow button else show follow
    curr_user = User.objects.get(username = request.user) 
    
    # Get count of followers
    get_follow= Follow.objects.get(user = get_user)
    get_follower_count = get_follow.follower.count() or  0
    get_following_count = get_user.following.count() or 0
    if hasattr(curr_user, "following"):
        # get the list of the user is following
        curr_following = curr_user.following.all()
        # loop check
        for follow in curr_following:
            str_user = str(follow.user)
            str_profile = str(get_user.username)
            if(str_user == str_profile):
                # if following
                is_following = True
        
    # Fileter the Post by User author
    posts = Post.objects.filter(author = get_id.author).order_by('-date')

    paginator = Paginator(posts, 10)
    
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    return render(request, "network/profile.html", {
        "posts":posts,
        "userId": get_userId,
        "nam":nam,
        "is_following": is_following,
        "following": get_following_count,
        "follower": get_follower_count
    })

        
# Profile of logged user
def profile_logged(request):
    
    posts = Post.objects.filter(author = request.user).order_by('-date')
    
    paginator = Paginator(posts, 10)
    
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    curr_user = User.objects.get(username = request.user)
    nam = str(curr_user.username)

    # Get count of followers
    get_followers= Follow.objects.get(user = curr_user)
    f_count = get_followers.follower.count() or  0
    get_following = curr_user.following.count() or 0
    print("this",get_following)
    return render(request, "network/profile.html", {
        "posts":posts,
        "nam": nam,
        "follower": f_count,
        "following": get_following
    })

# Get the Post of all the user is following
def following_post(request):
    logged_user = User.objects.get(pk = request.user.id)

    
    # get the list of the current user is following
    user_following = logged_user.following.all()
    following_post = []
    
    for name in user_following:
        check_post = Post.objects.filter(author__username = name.user).order_by('-date').annotate(lcount=Count('likes'))
        if(check_post):
            following_post.extend(check_post)
        
    # check if the current user liked the post
    user_liked = []
    like_list = Like.objects.all()
    try: 
        for like in like_list:
            if like.user.id == request.user.id:
                user_liked.append(like.post.id)
    except:
        user_liked = []
        
    # Paginator
    paginator = Paginator(following_post, 10)
  
    page_number = request.GET.get('page')
    postinator = paginator.get_page(page_number)
    print(following_post)
    return render(request, "network/following.html", {
        "posts": postinator,
        "likelist": user_liked,
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
        content =  Post.objects.get(id = post_id)
        print("this", data.get('content'))
        content.content = data.get('content')
        content.save()
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


def follow(request, id):
    if request.method == "POST":
        
        data = json.loads(request.body)
        userId = data["id"]

        curr_profile = User.objects.get(pk=userId)
        curr_user = request.user
        follower = User.objects.get(pk = curr_user.id)  

        # Check if User already exists
        if Follow.objects.filter(user = curr_profile):
            # get the current count of following and followers for profile
            get_following = curr_user.following.count()
            get_followers = Follow.objects.get(user = curr_user).follower.count()
            # Check if the current user is already following the user
            if hasattr(curr_user, "following"):
                # Check if the current profile is already in the currently logged in user list of following
                curr_following = curr_user.following.all() # get the list of the current logged user following
                str_curr_profile = str(curr_profile.username).lower()
                for follow in curr_following:
                    str_profile = str(follow.user).lower()
                    print(f"this str_profile: {str_profile}")
                    if(str_profile == str_curr_profile):
                        print("following")
                        return JsonResponse({"message": "already Following",
                                             "following": get_following,
                                             "followers": get_followers})
                # if user is not following the current profile       
                curr_follow = Follow.objects.get(user = curr_profile)
                curr_follow.follower.add(follower)
                curr_follow.save()
                
                # update the followers and following count
                get_followers = curr_follow.follower.count()
                get_following = curr_profile.following.count()
                return JsonResponse({"message": "followed",
                                     "following": get_following,
                                     "followers": get_followers})
        # Create a new follow object for the curr_profile
        else:
            return JsonResponse({"message":"not followed"})


def unfollow(request, id):
    if request.method == "POST":

        data = json.loads(request.body)
        userId = data["id"]
        
        curr_profile = User.objects.get(pk = id)
        curr_user = request.user
        follower = User.objects.get(pk = curr_user.id)
        
        # get follow object of the profile
        curr_follow = Follow.objects.get(user = curr_profile)
        curr_follow.follower.remove(follower)
        curr_follow.save()
        
        # get the current stat of following and followers
        get_followers = curr_follow.follower.count()
        get_following = curr_profile.following.count()
        
    return JsonResponse({"message":"None yet",
                         "followers":get_followers,
                         "following":get_following})
        
        
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

