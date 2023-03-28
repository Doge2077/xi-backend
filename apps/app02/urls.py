from django.urls import path

from app02 import views

urlpatterns = [
    path('headinfo/', views.head_info.as_view()),
    path('newsinfo/', views.get_news_info.as_view()),
    path('sentenceinfo/', views.daily_sentences.as_view()),
]