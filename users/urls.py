from django.urls import include, path
from . import views

urlpatterns = [
    path('me/', views.AccountView, name='account'),
    path('home/', views.HomeView, name='home'),
    path('spotify/', views.SpotifyView, name='spotify'),
    path('facebook/', views.FacebookView, name='facebook'),
]
