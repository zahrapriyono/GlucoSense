# core_api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Jalur untuk Artikel
    path('articles/', views.get_articles, name='get_articles'),
    
    # Jalur untuk Rekomendasi Dokter
    path('doctors/', views.get_doctors, name='get_doctors'),
]