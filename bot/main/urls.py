from django.urls import path

from . import views

urlpatterns = [
    path('link-updates', views.LinkUpdatesView.as_view())
]
