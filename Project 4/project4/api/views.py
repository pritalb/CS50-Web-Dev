from ast import And
from operator import truediv
from turtle import pos
from urllib import response
from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view

from network.models import Post, User

# Create your views here.

@api_view(['POST',])
@login_required
def create_new_post(request):
    data = request.data

    post_content = data['content']
    post = Post.objects.create(content=post_content, poster=request.user)
    post.save()
    
    return Response({'message': 'post created successfully.'})

@api_view(['GET'])
def get_all_posts(request):
    posts = Post.objects.all()
    posts_json = {}

    for post in posts:
        posts_json[post.pk] = {
            'content' : post.content,
            'likes' : post.likes,
            'post_user' : str(post.poster),
            'date_published' : post.date_published,
        }

    return Response(posts_json)

def edit_post(request, post_id):
    pass

@api_view(['GET'])
def get_user_profile(request, user_id):
    queried_user = User.objects.get(pk=user_id)
    follow_allowed = (request.user != queried_user) and (request.user.is_authenticated)
    user_posts_json = {}

    try:
        following = queried_user.following.all()
    except:
        following = {}

    try:
        followers = queried_user.followers.all()
    except:
        followers = {}

    try:
        user_posts = queried_user.posts.all()
    except:
        pass
    
    for post in user_posts:
        user_posts_json[post.pk] = {
            'content' : post.content,
            'likes' : post.likes,
            'post_user' : str(post.poster),
            'date_published' : post.date_published,
        }

    return Response({
        'name' : str(queried_user),
        'posts' : user_posts_json,
        'can_follow' : follow_allowed,
        'total_followers' : len(followers),
        'total_following' : len(following),
    })



@api_view(['PUT'])
@login_required
def follow_user(request, user_id):
    current_user = request.user
    user_to_follow = User.objects.get(pk=user_id)

    current_user.following.add(user_to_follow)
    current_user.save()

    return Response({'message': 'user followed successfully.'})

@api_view(['PUT'])
@login_required
def unfollow_user(request, user_id):
    current_user = request.user
    user_to_unfollow = User.objects.get(pk=user_id)

    current_user.following.remove(user_to_unfollow)
    current_user.save()

    return Response({'message': 'user unfollowed successfully.'})

@api_view(['PUT'])
@login_required
def like_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.likes += 1
    post.save()

    return Response({'message': 'post liked successfully.'})

@api_view(['PUT'])
@login_required
def unlike_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.likes -= 1
    post.save()

    return Response({'message': 'post unliked successfully.'})