from django.urls import path
from . import views


urlpatterns = [
    path('', views.service_index, name="service_index"),
    path('<service>/', views.service_detail, name="service_detail"),
]