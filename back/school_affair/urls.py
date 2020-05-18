from django.urls import path

from . import views

urlpatterns = [
    path('home', views.index),
    path('login', views.login),
    path('logout', views.logout),
    path('campus',views.campus),
    path('major',views.major),
    path('class',views.class_info)
]