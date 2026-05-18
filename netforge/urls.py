from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Home
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    
    # Apps
    path('academy/', include('academy.urls')),
    path('courses/', include(('courses.urls', 'courses'), namespace='courses')),
    path('labs/', include(('labs.urls', 'labs'), namespace='labs')),
    path('payments/', include(('payments.urls', 'payments'), namespace='payments')),
    path('accounts/', include(('users.urls', 'users'), namespace='accounts')),
]
