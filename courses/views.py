#from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.db import IntegrityError, transaction
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.forms.formsets import formset_factory
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils import timezone
from admin_app.models import Problem, Activity, CourseAsTaught, CourseDay, Course
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.models import Group, User
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from subprocess import Popen, PIPE, STDOUT
import subprocess
import os
import unicodedata
import logging
user = get_user_model()

# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)


def course_list(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        print('post', request.POST)
        course = CourseAsTaught(
            name=request.POST['name'], instructor=request.POST['instructor'], post=request.POST)
    else:
        # if a GET (or any other method) we'll create a blank day
        course = CourseAsTaught(name='Energy and Entropy', instructor="David", days=[
            CourseDay('Monday'),
            CourseDay('Wednesday'),
        ])
    courses = Course.objects.all().order_by('quarter_numbers')
    return render(request, 'courses/list.html', {
        'course': course,
        'courses': courses,
    })


def course_title(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course_title = course.title
    return HttpResponse(course_title)
