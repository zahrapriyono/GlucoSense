# core_api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.get_article_list, name='get_article_list'),
    path('articles/<int:article_id>/', views.get_article_detail, name='get_article_detail'),

    path('saved-articles/', views.saved_article_api, name='saved_article_api'),

    path('saved-articles/<int:article_id>/', views.delete_saved_article_api, name='delete_saved_article_api'),

    path('doctors/', views.get_doctor_list, name='get_doctor_list'),
    path('doctors/<int:doctor_id>/', views.get_doctor_detail, name='get_doctor_detail'),

    path('glucose-logs/', views.glucose_log_api, name='glucose_log_api'),

    path('food-logs/', views.food_log_api, name='food_log_api'),

    path('medical-profile/', views.medical_profile_api, name='medical_profile_api'),

    path('favorite-doctors/', views.favorite_doctor_api, name='favorite_doctor_api'),

    path('chat-history/', views.chat_history_api, name='chat_history_api'),

    path('chat/', views.chat_api, name='chat_api'),

    path('register/', views.register_api, name='register_api'),
    
    path('login/', views.login_api, name='login_api'),

    path('assessment/', views.submit_assessment_api, name='submit_assessment_api'),

    path('assessment/history/', views.get_assessment_history_api, name='assessment-history'),

    path('assessment/<int:assessment_id>/', views.get_assessment_detail_api, name='assessment-detail'),
]