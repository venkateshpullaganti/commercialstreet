from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def calculate():
    y = 4
    x = 3
    return x

def say_hello(request):
    x = calculate()
    print(x)
    return render(request, "hello.html",{"name":"Jarvis"})