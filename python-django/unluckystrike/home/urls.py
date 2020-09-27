from django.urls import path
from . import views


urlpatterns = [
    path("", views.home_index, name="home_index"),
    path("about", views.home_about, name="home_about"),
    path("contact", views.home_contact, name="home_contact"),
    path("works", views.home_works, name="home_works"),
    path("works/<work>", views.work_detail, name="work_detail"),
]