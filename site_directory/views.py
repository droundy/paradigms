from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import TemplateView, ListView, View
from admin_app.models import Problem, Figure, FigureAssociations, Activity, Sequence
from public_app.forms import ProblemForm
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.models import Group, User
from django.contrib.auth import get_user_model
user = get_user_model()
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from subprocess import Popen, PIPE, STDOUT
import subprocess, os
import unicodedata
import logging

def HomeworkSearchView(request):
    query = request.POST.get("q")
    search_type = request.POST.get("search_type")
    # print(search_type)
    # print(query)
    if search_type == "Homework" or search_type == "Both":
        # print("retrieving problems")
        problem_list = Problem.objects.filter(
            Q(problem_title__icontains=query) | Q(topics__icontains=query) | Q(course__icontains=query)
        )
        # print(problem_list)
    if search_type == "Activities" or search_type == "Both":
        # print("retrieving activities")
        activity_list = Activity.objects.filter(
            Q(title__icontains=query) | Q(topics__icontains=query) | Q(course__icontains=query) | Q(old_name__icontains=query) | Q(keywords__icontains=query) | Q(type_of_beast__icontains=query)        
        )
        sequence_list = Sequence.objects.filter(
            Q(title__icontains=query) | Q(overview_paragraph__icontains=query)
        )
        # print(activity_list)
    if search_type == "Activities":
        context = {
            'activity_list': activity_list,
            'search_type': search_type,
            'query': query,
        }
    if search_type == "Homework":
        context = {
            'problem_list': problem_list,
            'search_type': search_type,
            'query': query,
        }
    if search_type == "Both":
        context = {
            'problem_list': problem_list,
            'activity_list': activity_list,
            'sequence_list': sequence_list,
            'search_type': search_type,
            'query': query,
        }
    return render(request, 'directory/generic_search_results.html', context)

def HomeworkKeywordView(request, searchterm):
    query = searchterm
    print(query)
    problem_list = Problem.objects.filter(
        Q(problem_title__icontains=query) | Q(topics__icontains=query) | Q(course__icontains=query)
    )
    activity_list = Activity.objects.filter(
        Q(title__icontains=query) | Q(topics__icontains=query) | Q(course__icontains=query) | Q(old_name__icontains=query) | Q(keywords__icontains=query) | Q(type_of_beast__icontains=query)
    )
    sequence_list = Sequence.objects.filter(
        Q(title__icontains=query) | Q(overview_paragraph__icontains=query)
    )

    context = {
        'problem_list': problem_list,
        'activity_list': activity_list,
        'sequence_list': sequence_list,
        'search_type': 'Both',
        'query': query,
    }
    return render(request, 'directory/generic_search_results.html', context)
    # return render(request, 'directory/homework_search_results.html', context)