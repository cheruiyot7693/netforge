from django.shortcuts import render
from django.http import HttpResponse

def lab_list(request):
    """Display list of labs"""
    return render(request, 'labs/list.html')

def lab_detail(request, lab_id):
    """Display lab detail"""
    return render(request, 'labs/detail.html', {'lab_id': lab_id})

def lab_start(request, lab_id):
    """Start a lab"""
    return HttpResponse(f"Starting lab {lab_id}")

def session_list(request):
    """Display list of lab sessions"""
    return render(request, 'labs/sessions.html')

def session_detail(request, session_id):
    """Display session detail"""
    return render(request, 'labs/session_detail.html', {'session_id': session_id})

def automation_list(request):
    """Display automation tasks"""
    return render(request, 'labs/automation.html')

def automation_detail(request, task_id):
    """Display automation task detail"""
    return render(request, 'labs/automation_detail.html', {'task_id': task_id})

def monitoring_dashboard(request):
    """Display NOC monitoring dashboard"""
    return render(request, 'labs/monitoring.html')
