from django.shortcuts import render
from django.http import HttpResponse

def payment_list(request):
    """Display payment history"""
    return render(request, 'payments/list.html')

def checkout(request, course_id):
    """Handle course checkout"""
    return render(request, 'payments/checkout.html', {'course_id': course_id})

def payment_success(request):
    """Payment successful"""
    return render(request, 'payments/success.html')

def payment_cancel(request):
    """Payment cancelled"""
    return render(request, 'payments/cancel.html')
