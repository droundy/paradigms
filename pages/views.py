#from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

# class Home(TemplateView):
#         template_name = 'home.html'
def home(request):
        return render(request, 'pages/home.html', {})

class Loggedout(TemplateView):
        template_name = 'logout.html'

def white_papers(request):
        return render(request, 'pages/white_papers.html', {})

def about(request):
        return render(request, 'pages/about.html', {})

def history(request):
        return render(request, 'pages/history.html', {})

def courses(request):
        return render(request, 'pages/courses.html', {})

def selfedit(request):
        return render(request, 'pages/editable.html', {})