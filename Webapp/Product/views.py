from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request,'index.html')

def register(request):
    return render(request,'register.html')

def my_login(request):
    return render(request,'my-login.html')

def dashboard(request):
    return render(request,'dashboard.html')


