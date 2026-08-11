from django.urls import path
from . import views

app_name = 'assessment'

urlpatterns = [
    path('', views.form, name='form'),
    path('result/', views.result, name='result'),
    path('submit/', views.submit, name='submit'),
]