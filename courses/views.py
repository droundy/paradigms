#from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.db import IntegrityError, transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.forms.formsets import formset_factory
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils import timezone
from admin_app.models import Problem, Activity, CourseAsTaught, CourseAsTaughtOld, CourseDayOld, Course, CourseLearningOutcome, CourseDay
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
user = get_user_model()

# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)

def course_list(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        print('post', request.POST)
        course = CourseAsTaughtOld(
            name=request.POST['name'], instructor=request.POST['instructor'], post=request.POST)
    else:
        # if a GET (or any other method) we'll create a blank day
        course = CourseAsTaughtOld(name='Energy and Entropy', instructor="David", days=[
            CourseDayOld('Monday'),
            CourseDayOld('Wednesday'),
        ])
    courses = sorted(Course.objects.all(), key=lambda c: c.quarter_integer)
    return render(request, 'courses/list.html', {
        'course': course,
        'courses': courses,
    })

def course_as_taught(request, number, year, view='overview'):
    # if this is a POST request we need to process the form data
    course = get_object_or_404(Course, number=number)
    as_taught = get_object_or_404(CourseAsTaught, course=course, slug=year)
    days = CourseDay.objects.filter(taught=as_taught).order_by('number')
    return render(request, 'courses/taught.html', {
        'course': course,
        'taught': as_taught,
        'view': view,
        'days': days,
    })

@permission_required('admin_app.edit_course_as_taught',login_url='/')
def course_as_taught_edit(request, number, year):
    # if this is a POST request we need to process the form data
    course = get_object_or_404(Course, number=number)
    if year == 'NEW' and CourseAsTaught.objects.filter(course=course, slug='NEW').count() == 0:
        as_taught = CourseAsTaught(course=course, year='NEW', instructor=request.user.get_full_name())
        as_taught.save()
        print('creating new course')
    else:
        as_taught = get_object_or_404(CourseAsTaught, course=course, slug=year)
    
    if request.method == 'POST':
        as_taught.instructor = request.POST['instructor']
        as_taught.year = request.POST['year']
        as_taught.slug = as_taught.year.replace(' ', '')

        for day in CourseDay.objects.filter(taught=as_taught):
            if 'day-{}-delete'.format(day.pk) in request.POST:
                day.delete()
            else:
                day.day = request.POST['day-{}'.format(day.pk)]
                day.save()

        if request.POST['day-new'] != '':
            print('new day', request.POST['day-new'])
            new_day_number = 1
            last_day = CourseDay.objects.aggregate(django.db.models.Max('number'))
            if last_day['number__max'] is not None:
                new_day_number = last_day['number__max'] + 1
            newday = CourseDay(taught=as_taught, day=request.POST['day-new'], number=new_day_number)
            newday.save()
        as_taught.save()
        if as_taught.slug != year:
            return HttpResponseRedirect(django.urls.reverse('course_as_taught_edit', args=(number, as_taught.slug)))

    days = CourseDay.objects.filter(taught=as_taught).order_by('number')
    return render(request, 'courses/taught-edit.html', {
        'course': course,
        'taught': as_taught,
        'days': days,
    })

def course_view(request, number, view='overview'):
    # if this is a POST request we need to process the form data
    course = get_object_or_404(Course, number=number)
    print(dir(course))
    print(course.courseastaught_set.all())
    as_taught = CourseAsTaught.objects.filter(course=course)
    print(list(as_taught))
    return render(request, 'courses/view.html', {
        'course': course,
        'view': view,
    })

def course_title(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course_title = course.title
    return HttpResponse(course_title)
