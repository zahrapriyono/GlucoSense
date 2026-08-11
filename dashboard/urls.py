from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.profile, name='profile'),
    path('report/<int:report_id>/', views.report_detail, name='report_detail'),
]