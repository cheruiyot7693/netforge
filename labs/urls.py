from django.urls import path
from . import views

urlpatterns = [
    # Labs
    path('', views.lab_list, name='list'),
    path('<int:lab_id>/', views.lab_detail, name='detail'),
    path('<int:lab_id>/start/', views.lab_start, name='start'),
    path('<int:lab_id>/export/containerlab/', views.export_containerlab, name='export_containerlab'),
    path('<int:lab_id>/export/vrnetlab/', views.export_vrnetlab, name='export_vrnetlab'),
    
    # Lab Sessions
    path('sessions/', views.session_list, name='session_list'),
    path('sessions/<int:session_id>/', views.session_detail, name='session_detail'),
    
    # Automation Engine
    path('automation/', views.automation_list, name='automation_list'),
    path('automation/<int:task_id>/', views.automation_detail, name='automation_detail'),
    
    # Monitoring/NOC
    path('monitoring/', views.monitoring_dashboard, name='monitoring'),
]
