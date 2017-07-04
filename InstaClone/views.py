# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from forms import SignUpForm, LoginForm, PostForm, LikeForm, CommentForm
from models import UserModel, SessionToken, PostModel, LikeModel, CommentModel
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login, logout, get_user_model
from datetime import timedelta
from django.utils import timezone

import cloudinary
import cloudinary.uploader
import cloudinary.api

# Create your views here.

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            #saving data to DB
            user = UserModel(name=name, password=make_password(password), email=email, username=username)
            user.save()
            return render(request, 'success.html')
            #return redirect('login/')
    else:
        form = SignUpForm()

    return render(request, 'index.html', {'form' : form})


def login_view(request):
    dict = {}
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = UserModel.objects.filter(username=username).first()

            if user:
                # Check for the password
                print make_password(password), user.password
                if not check_password(password, user.password):
                    dict['message'] = 'Incorrect Password! Please try again!'
                else:
                    token = SessionToken(user=user)
                    token.create_token()
                    token.save()
                    response = redirect('feed/')
                    response.set_cookie(key='session_token', value=token.session_token)
                    return response
    else:
        form = LoginForm()

    dict['form'] = form
    return render(request, 'login.html', dict)

def feed_view(request):
    user = check_validation(request)
    if user:

        feeds = PostModel.objects.all().order_by('created_on')
        # TODO 1: DETERMINE IF CURRENT USER HAS LIKED ON EACH POST
        # TODO 2: GET TOTAL LIKES ON EACH POST
        # TODO 3: GET ALL COMMENTS FOR EACH POST

        return render(request, 'feed.html', {feeds: feeds})
    else:

        return redirect('/login/')

def post_view(request):
    user = check_validation(request)
    if user:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                # TODO: ADD CLOUDINARY
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')

                post = PostModel(user=user, image=image, caption=caption)
                post.save()
                return redirect('/feed/')
        else:
            form = PostForm()
        return render(request, 'post.html', {'form' : form})
    else:
        return redirect('/login/')

<<<<<<< HEAD

def like_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post')
            has_already_liked = LikeModel.objects.filter(post_id=post_id, user=user).first()
            if not has_already_liked:
                LikeModel.objects.create(post_id=post_id, user=user)
            else:
                has_already_liked.delete()

            return redirect('/feed/')

    else:
        return redirect('/login/')


def comment_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post')
            comment_text = form.cleaned_data.get('comment_text')
            CommentModel.objects.create(user=user, post_id=post_id, comment_text=comment_text)
            # TODO: ADD MESSAGE TO INDICATE SUCCESS
            return redirect('/feed/')
        else:
            # TODO: ADD MESSAGE FOR FAILING TO POST COMMENT
            return redirect('/feed/')
    else:
        return redirect('/login')

=======
def like_view(request):
    user = check_validation(request)
    if user:
        image =
        if request.method == "POST":
>>>>>>> 737bcc28e0d2cfb27558a4a70c6b497b33c8f6e3


#For validating the session
def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            time_to_live = session.created_on + timedelta(days=1)
            if time_to_live > timezone.now():
                return session.user
    else:
        return None


