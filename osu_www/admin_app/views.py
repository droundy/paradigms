from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    #return HttpResponse("This is the home page")
    return render(request, 'admin_app/index.html', {})

def problem_list(request):
    return render(request, 'admin_app/problem_list.html', {})

# def white_papers(request):
#     return render(request, 'admin_app/white_papers.html', {})
