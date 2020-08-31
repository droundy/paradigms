#from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from admin_app.models import Activity, ActivityMedia, MediaAssociation, Sequence, SequenceItems
from activities.forms import ActivityForm, ActivityFormReadOnly
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
from django_tex.shortcuts import render_to_pdf

@permission_required('admin_app.can_edit_activity',login_url='/')
def activity_new(request):
    if request.method == "POST":
        form = ActivityForm(request.POST, request.FILES)
        if form.is_valid():
            messages.error(request, 'Activity Added')
            activity = form.save(commit=False)
            # problem.author = request.user
            activity.publication_date = timezone.now()
            activity.save()
            form.save_m2m()
            return redirect('activity_detail', pk=activity.pk)
        else:
            messages.error(request, 'Activity Saved')
            messages.error(request, form.errors)
            messages.error(request, 'Activity Saved')
    else:
        context = {
            'author': request.user.pk,
            'time_estimate': '5',
            'type_of_beast': 'Small Group Activity',
            'publication_status': 'Draft',
            'page_title': 'Add Activity', 
        }
        form = ActivityForm(context)
    return render(request, 'activities/activity_edit.html', {'form': form, 'page_title': 'Add Activity'})

@permission_required('admin_app.can_edit_activity',login_url='/')
def activity_edit(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    this_key = pk
    print(activity.title)
    if request.method == "POST":
        # messages.error(request, 'POSTED')
        form = ActivityForm(request.POST, request.FILES, instance=activity)
        if form.is_valid():
            messages.error(request, 'Activity Saved')
            activity = form.save(commit=False)
            # problem.author = request.user
            activity.publication_date = timezone.now()
            activity.save()
            form.save_m2m()
            return redirect('activity_edit', pk=activity.pk)
        else:
            messages.error(request, form.errors)
            #return redirect('problem_edit_preview', pk=problem.pk)
    else:
        form = ActivityForm(instance=activity)
        thisPrimaryKey = activity.pk
        figures_list = Activity.objects.get(id=thisPrimaryKey).media.all()
        context = {
            'thisPrimaryKey': thisPrimaryKey,
            'form': form,
            'figures': figures_list,
            'activity': activity,
            'this_key': this_key,
            'page_title': activity.title + ' - Edit',
        }
    return render(request, 'activities/activity_edit.html', context)

def activity_list(request):
    if request.user.has_perm("admin_app.change_problem"):
        activities = Activity.objects.all().order_by('title')
    else:
        activities = Activity.objects.filter(publication_status='Published').order_by('title')
    return render(request, 'activities/activity_list.html', {'activities': activities, 'page_title': 'Paradigms Activity List'})

def activity_title(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    activity_title = activity.title
    return HttpResponse(activity_title)

def activity_detail(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    this_key = pk
    figures_list = Activity.objects.get(id=this_key).media.all()
    view_name = 'activity_detail'
    form = ActivityFormReadOnly(instance=activity)

    # Find the sequence(s) in which this Activity has been assigned
    if request.user.has_perm("admin_app.change_problem"):
        activity_sequences = Sequence.objects.filter(activities=activity)
    else:
        activity_sequences = Sequence.objects.filter(activities=activity).filter(publication="1")

    context = {
        'activity': activity,
        'latex': activity.guide_latex,
        'activity_sequences': activity_sequences,
        'this_key': this_key,
        'form': form,
        'view_name': view_name,
        'figures': figures_list,
        'page_title': activity.title,
    }
    return render(request, 'activities/activity_detail.html', context)

def activity_detail_solution(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    this_key = pk
    view_name = 'activity_detail_solution'
    form = ActivityFormReadOnly(instance=activity)
    context = {
        'activity': activity,
        'latex': activity.solution_latex,
        'this_key': this_key,
        'form': form,
        'view_name': view_name,
        'page_title': activity.title + ' - Solution',
    }
    return render(request, 'activities/activity_detail.html', context)

def activity_detail_handout(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    this_key = pk
    view_name = 'activity_detail_handout'
    form = ActivityFormReadOnly(instance=activity)
    context = {
        'activity': activity,
        'latex': activity.handout_latex,
        'this_key': this_key,
        'form': form,
        'view_name': view_name,
        'page_title': activity.title + ' - Handout',
    }
    return render(request, 'activities/activity_detail.html', context)

def activity_pdf_guide(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    this_key = pk
    figures_list = Activity.objects.get(id=this_key).media.all()
    form = ActivityFormReadOnly(instance=activity)

    # Find the sequence(s) in which this Activity has been assigned
    if request.user.has_perm("admin_app.change_problem"):
        activity_sequences = Sequence.objects.filter(activities=activity)
    else:
        activity_sequences = Sequence.objects.filter(activities=activity).filter(publication="1")

    context = {
        'activity': activity,
        'latex': activity.guide_latex,
        'activity_sequences': activity_sequences,
        'this_key': this_key,
        'form': form,
        'view_name': "Instructor's guide",
        'figures': figures_list,
        'page_title': activity.title,
    }
    return render_to_pdf(request, 'activities/activity.tex', context, filename='instructor-guide.pdf')

def activity_pdf_solution(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    context = {
        'activity': activity,
        'latex': activity.solution_latex,
        'view_name': 'Solution',
    }
    return render_to_pdf(request, 'activities/activity.tex', context, filename='solution.pdf')

def activity_pdf_handout(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    context = {
        'activity': activity,
        'latex': activity.pdf_handout_latex,
        'view_name': 'Handout',
    }
    return render_to_pdf(request, 'activities/activity.tex', context, filename='handout.pdf')
