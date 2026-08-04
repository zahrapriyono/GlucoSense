from django.urls import path
from . import views

app_name = 'doctors'

urlpatterns = [
    path('', views.list_doctors, name='list'),
]