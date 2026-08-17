from django.urls import path
from .  import views

app_name = 'knowledge'

urlpatterns = [
    path('', views.list_articles, name='list'),
    path('<int:article_id>/', views.detail, name='detail')
]