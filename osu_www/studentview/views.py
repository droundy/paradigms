from django.core.files.storage import FileSystemStorage
from django.db import IntegrityError, transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.forms.formsets import formset_factory
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils import timezone
from admin_app.models import Problem, Activity, CourseAsTaught, Course, CourseLearningOutcome, CourseDay, DayActivity, DayProblem
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.models import Group, User
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import django
from subprocess import Popen, PIPE, STDOUT
import subprocess
import os
import unicodedata
import logging
import django_tex, latex_snippet
from django_tex.shortcuts import render_to_pdf
user = get_user_model()

# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)

def home(request):
    courses = sorted(CourseAsTaught.objects.all(), key=lambda c: c.course.quarter_integer)
    return render(request, 'studentview/home.html', {
        'as_taughts': courses,
    })

def problem_set(request, number, year, problemset, view='html'):
    course = get_object_or_404(Course, number=number)
    as_taught = get_object_or_404(CourseAsTaught, course=course, slug=year)
    day = None
    for d in CourseDay.objects.filter(taught=as_taught).order_by('order'):
        if d.problemset_slug == problemset or d.pk == problemset:
            day = d
            break
    if day is None:
        which = 1
        for d in CourseDay.objects.filter(taught=as_taught).order_by('order'):
            day = d
            if 'hw'+str(which) == problemset:
                break
            which += 1
    context = {
        'course': course,
        'taught': as_taught,
        'view': view,
        'day': day,
    }
    if view == 'pdf':
        return render_to_pdf(request, 'courses/problemset.tex', context, filename=d.problemset_slug+'.pdf')
    elif view == 'solution-pdf':
        return render_to_pdf(request, 'courses/problemset.tex', context, filename=d.problemset_slug+'-solution.pdf')
    else:
        return render(request, 'studentview/problemset.html', context)

def handout(request, pk, view='html'):
    da = get_object_or_404(DayActivity, pk=pk)
    day = da.day
    as_taught = day.taught
    course = as_taught.course
    context = {
        'course': course,
        'taught': as_taught,
        'view': view,
        'day': day,
        'activity': da.activity,
        'da': da,
        'view_name': 'Handout'
    }
    if view == 'pdf':
        context['latex'] = da.activity.pdf_handout_latex
        return render_to_pdf(request, 'activities/activity.tex', context, filename='handout.pdf')
    elif view == 'solution-pdf':
        context['latex'] = da.activity.solution_latex
        context['view_name'] = 'Solution'
        return render_to_pdf(request, 'activities/activity.tex', context, filename='solution.pdf')
    else:
        return render(request, 'studentview/handout.html', context)

def schedule(request, number, year, view='overview'):
    # if this is a POST request we need to process the form data
    course = get_object_or_404(Course, number=number)
    if year == 'latest':
        as_taught = CourseAsTaught.objects.filter(course=course).order_by('-pk').first()
    else:
        as_taught = get_object_or_404(CourseAsTaught, course=course, slug=year)
    days = list(CourseDay.objects.filter(taught=as_taught).order_by('order'))
    learning_outcomes = list(CourseLearningOutcome.objects.filter(course=course))
    for l in learning_outcomes:
        l.my_activities = Activity.objects.filter(day__taught=as_taught, learning_outcomes=l)
        l.my_problems = Problem.objects.filter(day__taught=as_taught, learning_outcomes=l)
    for d in days:
        for a in Activity.objects.filter(day=d):
            if a.readings != '':
              d.resources += '\n\n' + a.readings
    return render(request, 'studentview/view.html', {
        'course': course,
        'taught': as_taught,
        'view': view,
        'days': days,
        'learning_outcomes': learning_outcomes,
    })
