from django.urls import path

from . import views

urlpatterns = [
    path('home', views.index),
    path('login', views.login),
    path('logout', views.logout),
    path('campus',views.campus),
    path('major',views.major),
    path('class',views.class_info),
    path('student',views.student_info),
    path('teacher',views.teacher_info),
    path('unnormal',views.student_unnormal_change),
    path('course',views.course),
    path('course_sign_up',views.course_sign_up)

]