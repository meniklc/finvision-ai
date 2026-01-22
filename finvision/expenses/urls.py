from django.urls import path
from .views import dashboard, monthly_dashboard

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('monthly-dashboard/', monthly_dashboard, name='monthly_dashboard'),
]
