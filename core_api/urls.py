# core_api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.get_article_list, name='get_article_list'),
    path('doctors/', views.get_doctor_list, name='get_doctor_list'),
    path('glucose-logs/', views.glucose_log_api, name='glucose_log_api'),
    path('food-logs/', views.food_log_api, name='food_log_api'),
    path('medical-profile/', views.medical_profile_api, name='medical_profile_api'),
    path('favorite-doctors/', views.favorite_doctor_api, name='favorite_doctor_api'),
    path('chat-history/', views.chat_history_api, name='chat_history_api'),
    path('register/', views.register_api, name='register_api'),
    path('login/', views.login_api, name='login_api'),
]