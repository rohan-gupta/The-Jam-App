import base64
import requests

def getSpotifyTokens(code, redirect_uri, client_id, client_secret):
    endpoint = "https://accounts.spotify.com/api/token"
    body = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri
    }
    headers = {
        "Content-Type" : "application/x-www-form-urlencoded",
        "Authorization": "Basic " + base64.b64encode((client_id + ":" + client_secret).encode()).decode()
    }

    response = requests.post(endpoint, data=body, headers=headers)
    response = response.json()

    return response


def refreshSpotifyAccessToken(refresh_token, client_id, client_secret):
    endpoint = "https://accounts.spotify.com/api/token"
    body = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    headers = {
        "Content-Type" : "application/x-www-form-urlencoded",
        "Authorization": "Basic " + base64.b64encode((client_id + ":" + client_secret).encode()).decode()
    }

    response = requests.post(endpoint, data=body, headers=headers)
    response = response.json()

    # Response form recieved
    # {'access_token': 'BQCvY7Iex9v7oHGLlcFJ9cHxdNdzFVlxtRhPE_WaVw_wD9AghV7I3Z9oFpAcp2mSKD3NZ5wMLisPceF2oMBFZk0oNHg-EXIH2L0j7PJ__v2brg3Se3GV3KkMQOI4aVbuXXiZy5gMWIDeN14LxiZP-Xy9gFcQHWkuCO5xXPRvmj0uOFWBPl81S2CaB50JGOqsro8Y6q7ZweBtmLo5hBDQP5QLk6Z_', 'token_type': 'Bearer', 'expires_in': 3600, 'scope': 'playlist-read-private user-library-read user-follow-read playlist-modify-private user-read-email'}
    
    return response


def getSpotifyUserDetails(access_token):
    endpoint = "https://api.spotify.com/v1/me"
    headers = {
        "Authorization" : "Bearer " + access_token
    }

    response = requests.get(endpoint, headers=headers)
    response = response.json()

    return response
