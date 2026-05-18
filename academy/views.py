from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    context = {
        'title': 'NetForge Academy - Dashboard',
    }
    return render(request, 'academy/dashboard.html', context)
