from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('delete-city/', views.delete_city),
]
