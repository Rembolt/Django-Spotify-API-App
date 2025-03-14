from django.urls import path
from . import views

app_name = 'shuffle'

urlpatterns= [
    path("", views.index, name="index"),
    path("signout", views.appHandler.signOut, name="signout"),
    path("authorize/", views.authorize, name="authorize"),
    path("playlist", views.getPlaylist, name="playlist"),
    path("queue/<str:shuffle>", views.postPlaylist, name="queue"),
]