"""back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.shortcuts import render

def vue_login(request):
    return  render(request, 'login.html')
def vue_campus(request):
    return  render(request, 'campus.html')
def vue_major(request):
    return  render(request, 'major.html')
def vue_class(request):
    return  render(request, 'class.html')
def vue_student (request):
    return  render(request, 'student.html')
def vue_teacher(request):
    return  render(request, 'teacher.html')
def vue_manage_course(request):
    return  render(request, 'manage_course.html')
def vue_student_course(request):
    return  render(request, 'student_course.html')
def vue_teacher_course(request):
    return  render(request, 'teacher_course.html')
def vue_unnormal_change(request):
    return  render(request, 'unnormal_change.html')
urlpatterns = [
    path('api/', include('school_affair.urls')),
    path('admin/', admin.site.urls),
    path('login',vue_login),
    path('campus',vue_campus),
    path('major',vue_major),
    path('class',vue_class),
    path('student',vue_student),
    path('teacher',vue_teacher),
    path('manage_course',vue_manage_course),
    path('student_course',vue_student_course),
    path('teacher_course',vue_student_course),
    path('unnormal_change',vue_unnormal_change),
]
