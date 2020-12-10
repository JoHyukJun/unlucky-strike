from django.urls import path
from . import views


urlpatterns = [
    path("", views.home_index, name="home_index"),
    path("about", views.home_about, name="home_about"),
    path("contact", views.home_contact, name="home_contact"),
]