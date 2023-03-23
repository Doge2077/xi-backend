from django.urls import path

from app03 import views

urlpatterns = [
    path('category/', views.category.as_view()),
]