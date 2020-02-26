from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import urlencode
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm

from .models import User, SpotifyUser

import os
import requests

from .utils import *

# Reading enviroment variables
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")


# Create your views here.
def SignupView(request):

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(request, username=username, password=password)
            login(request, user)

        return HttpResponseRedirect(reverse('account'))

    else:
        form = CustomUserCreationForm()
        context = {
            'form': form
        }

        return render(request, 'registration/signup.html', context)


@login_required
def AccountView(request):

    spotify_connected = False
    facebook_connected = False

    if request.method == "GET":
        try:
            spotifyuser = SpotifyUser.objects.get(user__pk=request.user.pk)
            spotify_connected = True
        except:
            spotify_connected = False

    context = {
        'spotify_connected': spotify_connected,
        'facebook_connected': facebook_connected
    }

    return render(request, 'users/account.html', context)


@login_required
def HomeView(request):

    return render(request, 'users/home.html')


def SpotifyLoginView(request):

    params = {
        "client_id": SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "scope": "playlist-read-private user-library-read user-follow-read user-read-email",
        "state": request.session.get("_auth_user_hash")
    }
    params = urlencode(params)
    auth_endpoint = f"https://accounts.spotify.com/authorize?{params}"

    return redirect(auth_endpoint)


def SpotifyCallbackView(request):

    if request.GET.get("state") == request.session.get("_auth_user_hash"):
        if "code" in request.GET:
            code = request.GET.get("code")

            # Get access token and refresh token
            response = getSpotifyTokens(code, SPOTIFY_REDIRECT_URI, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
            request.session["spotify_access_token"] = response["access_token"]
            request.session["spotify_token_expires_in"] = 3600
            refresh_token = response["refresh_token"]

            # Get spotify user details
            response = getSpotifyUserDetails(request.session["spotify_access_token"])
            user = User.objects.get(pk=request.user.pk)
            spotifyuser = SpotifyUser(
                user=user,
                spotify_email=response["email"],
                spotify_name=response["display_name"],
                spotify_id=response["id"],
                refresh_token=refresh_token
            )
            spotifyuser.save()

        elif "error" in request.GET:
            error = request.GET.get("error")

    return redirect(reverse('account'))



def FacebookLoginView(request):

    print('Facebook button clicked')

    return render(request, 'users/account.html')
