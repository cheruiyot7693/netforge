from django.shortcuts import render
from django.http import HttpResponse

def course_list(request):
    """Display list of courses"""
    return render(request, 'courses/list.html')

def course_detail(request, course_id):
    """Display course detail"""
    return render(request, 'courses/detail.html', {'course_id': course_id})

def course_enroll(request, course_id):
    """Enroll user in course"""
    return HttpResponse(f"Enrolled in course {course_id}")
