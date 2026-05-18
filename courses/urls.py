from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='list'),
    path('<int:course_id>/', views.course_detail, name='detail'),
    path('<int:course_id>/enroll/', views.course_enroll, name='enroll'),
]
