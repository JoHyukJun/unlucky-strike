from django.urls import path
from . import views


urlpatterns = [
    path("", views.home_index, name="home_index"),
    path("work/<work>", views.work_detail, name="work_detail"),
]