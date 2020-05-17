from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate  
from django.contrib.auth import login as django_login
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@require_POST
def login(request):
    username = request.POST.get('username')
    #print(username)
    password = request.POST.get('password')
    #print(password)
    user = authenticate(username=username, password=password)
    
    if user is not None:
        django_login(request,user)
        #print(user.person)
        if  user.person: 
            return HttpResponse("welcome"+str(user.person))
        else :
            return HttpResponse("welcome Manager")
    else:
        return HttpResponse("login fail")
# Create your views here.


