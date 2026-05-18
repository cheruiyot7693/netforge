from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment_list, name='list'),
    path('checkout/<int:course_id>/', views.checkout, name='checkout'),
    path('success/', views.payment_success, name='success'),
    path('cancel/', views.payment_cancel, name='cancel'),
]
