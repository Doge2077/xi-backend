from django.urls import path
from app01 import views

urlpatterns = [
    path('login/', views.Login.as_view()),
    path('confirm/', views.Confirm.as_view()),
]