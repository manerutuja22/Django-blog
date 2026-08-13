# from django.http import HttpResponse 
from django.shortcuts import render

def home(request):
  # return HttpResponse('<h2>Home page </h2>')
  return render(request, 'home.html')