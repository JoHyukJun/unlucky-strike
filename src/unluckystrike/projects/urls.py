from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_index, name="project_index"),
    path('fishingram', views.Fishingram.as_view(), name="fishingram"),
    path('<project>', views.project_detail, name="project_detail"),
]