from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_index, name="project_index"),
    path('<project>', views.project_detail, name="project_detail"),
    path('etf/', views.etf_view, name='etf'),
    path('etf/<int:etf_id>/', views.etf_detail_view, name='etf_detail'),
]