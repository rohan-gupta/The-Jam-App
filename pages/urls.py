from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.IndexView, name='index'),
    path('about/', views.AboutView, name='about'),
    path('feedback/', views.FeedbackView, name='feedback'),
]
