from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    is_student = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    level = models.CharField(max_length=50, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('isp', 'ISP Level')
    ])
    duration_hours = models.IntegerField(default=10)
    price = models.IntegerField(default=0)  # in KSh
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Lab(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='labs')
    title = models.CharField(max_length=200)
    description = models.TextField()
    topology_type = models.CharField(max_length=100, default="nokia_single")
    difficulty = models.CharField(max_length=20, choices=[
        ('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')
    ])
    estimated_time = models.IntegerField(default=30)  # minutes

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    progress = models.IntegerField(default=0)  # percentage

    class Meta:
        unique_together = ('user', 'course')


class LabSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.lab.title}"
