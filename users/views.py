from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import urlencode
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm

from .models import User, SpotifyUser

import os
import requests

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

    spotify_connected = ''
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


def SpotifyView(request):

    if request.method == "GET" and request.GET.get("code"):
        try:
            spotifyuser = SpotifyUser.objects.get(user__pk=request.user.pk)
        except:
            # Request for access token and refresh token
            auth_code = request.GET.get("code")
            params = {
                "grant_type": "authorization_code",
                "code": auth_code,
                "redirect_uri": SPOTIFY_REDIRECT_URI,
                "client_id": SPOTIFY_CLIENT_ID,
                "client_secret": SPOTIFY_CLIENT_SECRET,
            }

            request_endpoint = "https://accounts.spotify.com/api/token"
            response = requests.post(request_endpoint, data=params)
            response = response.json()

            access_token = response["access_token"]
            refresh_token = response["refresh_token"]

            print(access_token)

            # Request for user's spotify account details
            headers = {"Authorization": "Bearer " + access_token}

            request_endpoint = "https://api.spotify.com/v1/me"
            response = requests.get(request_endpoint, headers=headers)
            response = response.json()

            spotifyuser = SpotifyUser(user=request.user, spotify_email=response["email"], spotify_name=response["display_name"], spotify_id=response["id"], refresh_token=refresh_token)
            spotifyuser.save()

        return redirect(reverse('account'))

    else:
        params = {
            "client_id": SPOTIFY_CLIENT_ID,
            "response_type": "code",
            "redirect_uri": SPOTIFY_REDIRECT_URI,
            "scope": "playlist-read-private user-library-read user-follow-read user-read-email",
        }
        params = urlencode(params)
        auth_endpoint = "https://accounts.spotify.com/authorize?%s" % (params)

        return redirect(auth_endpoint)


def FacebookView(request):

    print('Facebook button clicked')

    return render(request, 'users/account.html')
