from django.urls import path
from .  import views

app_name = 'knowledge'

urlpatterns = [
    path('', views.list_articles, name='list'),
    path('<slug:slug>/', views.detail, name='detail')
]