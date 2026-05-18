from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from academy.models import Course, Enrollment

def course_list(request):
    """Display list of courses with filtering and search"""
    courses = Course.objects.filter(is_active=True).order_by('-created_at')
    
    # Filter by level
    level = request.GET.get('level')
    if level:
        courses = courses.filter(level=level)
    
    # Search by title or description
    search = request.GET.get('search')
    if search:
        courses = courses.filter(
            title__icontains=search
        ) | courses.filter(
            description__icontains=search
        )
    
    # Get user's enrollments
    user_enrollments = []
    if request.user.is_authenticated:
        user_enrollments = Enrollment.objects.filter(
            user=request.user
        ).values_list('course_id', flat=True)
    
    context = {
        'courses': courses,
        'user_enrollments': list(user_enrollments),
        'selected_level': level,
        'search_query': search or '',
        'levels': [
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
            ('isp', 'ISP Level')
        ]
    }
    return render(request, 'courses/list.html', context)

def course_detail(request, course_id):
    """Display course detail"""
    course = get_object_or_404(Course, id=course_id, is_active=True)
    
    # Check if user is enrolled
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(
            user=request.user,
            course=course
        ).exists()
    
    context = {
        'course': course,
        'is_enrolled': is_enrolled,
        'labs': course.labs.all(),
    }
    return render(request, 'courses/detail.html', context)

@login_required(login_url='accounts:login')
def course_enroll(request, course_id):
    """Enroll user in course"""
    course = get_object_or_404(Course, id=course_id, is_active=True)
    
    # Check if already enrolled
    if Enrollment.objects.filter(user=request.user, course=course).exists():
        messages.warning(request, f'You are already enrolled in {course.title}')
        return redirect('courses:detail', course_id=course_id)
    
    # Create enrollment
    Enrollment.objects.create(user=request.user, course=course)
    messages.success(request, f'Successfully enrolled in {course.title}!')
    return redirect('courses:detail', course_id=course_id)
