#from django.shortcuts import render
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
user = get_user_model()

# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)

def course_list(request):
    courses = sorted(Course.objects.all(), key=lambda c: c.quarter_integer)
    return render(request, 'courses/list.html', {
        'courses': courses,
    })

def course_as_taught(request, number, year, view='overview'):
    # if this is a POST request we need to process the form data
    course = get_object_or_404(Course, number=number)
    as_taught = get_object_or_404(CourseAsTaught, course=course, slug=year)
    days = CourseDay.objects.filter(taught=as_taught).order_by('order')
    learning_outcomes = list(CourseLearningOutcome.objects.filter(course=course))
    for l in learning_outcomes:
        l.my_activities = Activity.objects.filter(day__taught=as_taught, learning_outcomes=l)
    return render(request, 'courses/taught.html', {
        'course': course,
        'taught': as_taught,
        'view': view,
        'days': days,
        'learning_outcomes': learning_outcomes,
    })

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
                day.topic = request.POST['day-{}-topic'.format(day.pk)]
                day.resources = request.POST['day-{}-resources'.format(day.pk)]
                day.order = request.POST['day-{}-order'.format(day.pk)]
                day.problemsetname = request.POST['day-{}-problemset'.format(day.pk)]
                for da in day.dayactivity_set.all():
                    if "day-{}-activity-{}-delete".format(day.pk, da.pk) in request.POST:
                        day.dayactivity_set.remove(activity)
                    da.show_handout = "day-{}-activity-{}-handout".format(day.pk, da.pk) in request.POST
                    da.show_solution = "day-{}-activity-{}-solution".format(day.pk, da.pk) in request.POST
                    da.order = request.POST["day-{}-activity-{}-order".format(day.pk, da.pk)]
                    da.save()
                for dp in day.dayproblem.all():
                    if "day-{}-problem-{}-delete".format(day.pk, dp.pk) in request.POST:
                        dp.delete()
                day.save()
                for dp in day.dayproblem.all():
                    dp.instructions = request.POST["day-{}-problem-{}-instructions".format(day.pk, dp.pk)]
                    dp.order = request.POST["day-{}-problem-{}-order".format(day.pk, dp.pk)]
                    duename = "day-{}-problem-{}-due".format(day.pk, dp.pk)
                    if duename in request.POST:
                        due = CourseDay.objects.filter(problemsetname=request.POST[duename]).first()
                        if due is not None:
                            dp.due = due
                    dp.save()
                new = "day-{}-activity-new".format(day.pk)
                if new in request.POST and request.POST[new] != '':
                    activity = get_title(day.taught.possible_activities, Activity.objects, request.POST[new])
                    order = next_order(day.dayactivity_set)
                    da = DayActivity(day=day, activity=activity, order=order)
                    da.save()
                new = "day-{}-problem-new".format(day.pk)
                if new in request.POST and request.POST[new] != '':
                    problem = get_problem_title(day.taught.possible_problems, Problem.objects, request.POST[new])
                    if problem is not None:
                        order = next_order(day.dayproblem)
                        dp = DayProblem(day=day, problem=problem, order=order, due=day)
                        dp.save()
                    else:
                        print('could not find problem')

        if request.POST['day-new'] != '':
            new_day_number = '001'
            order = next_order(CourseDay.objects.filter(taught=as_taught))
            newday = CourseDay(taught=as_taught, day=request.POST['day-new'], order=new_day_number)
            newday.save()
        as_taught.save()
        if as_taught.slug != year:
            return HttpResponseRedirect(django.urls.reverse('course_as_taught_edit', args=(number, as_taught.slug)))

    days = CourseDay.objects.filter(taught=as_taught).order_by('order')
    return render(request, 'courses/taught-edit.html', {
        'course': course,
        'taught': as_taught,
        'days': days,
    })

def next_order(query):
    l = list(query.order_by('order'))
    if len(l) > 0:
        try:
            return '%02d' % (int(l[-1].order)+1)
        except:
            return l[-1].order + 'x'
    return '01'

def get_title(query, all, key):
    o = query.filter(title=key).first()
    if o is not None:
        return o
    o = all.filter(title=key).first()
    if o is not None:
        return 0
    return all.filter(pk=key).get()

def get_problem_title(query, all, key):
    o = query.filter(problem_title=key).first()
    if o is not None:
        return o
    o = all.filter(problem_title=key).first()
    if o is not None:
        return 0
    try:
        return all.filter(pk=key).first()
    except:
        return None

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
    return render(request, 'courses/problemset.html', {
        'course': course,
        'taught': as_taught,
        'view': view,
        'day': day,
    })

def course_view(request, number, view='overview'):
    # if this is a POST request we need to process the form data
    course = get_object_or_404(Course, number=number)
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
