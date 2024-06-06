from django.urls import path

from . import views

urlpatterns = [
    path('chats', views.ChatApiView.as_view()),
    path('links', views.LinkApiView.as_view())
]
