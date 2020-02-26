from django.urls import include, path
from . import views

urlpatterns = [
    path('me/', views.AccountView, name='account'),
    path('home/', views.HomeView, name='home'),
    path('spotify/login/', views.SpotifyLoginView, name='spotify login'),
    path('spotify/callback/', views.SpotifyCallbackView, name='spotify callback'),
    path('facebook/login/', views.FacebookLoginView, name='facebook login'),
]
