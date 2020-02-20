#from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from admin_app.models import Activity, ActivityMedia, MediaAssociation
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

@permission_required('admin_app.can_edit_activity',login_url='/')
def activity_new(request):
    # problem = get_object_or_404(Problem, pk=pk)
    if request.method == "POST":
        # logging.debug('FORM POSTED')
        messages.error(request, 'ONEONEONE')
        form = ActivityForm(request.POST, request.FILES)
        if form.is_valid():
            messages.error(request, 'TWOTWOTWO')
            activity = form.save(commit=False)
            # problem.author = request.user
            activity.publication_date = timezone.now()
            activity.save()
            return redirect('activity_detail', pk=activity.pk)
        else:
            messages.error(request, form.errors)
            #return redirect('problem_edit_preview', pk=problem.pk)
    else:
        form = ActivityForm()
    return render(request, 'activities/activity_edit.html', {'form': form})

@permission_required('admin_app.can_edit_activity',login_url='/')
def activity_edit(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    this_key = pk
    if request.method == "POST":
        messages.error(request, 'POSTED')
        form = ActivityForm(request.POST, request.FILES, instance=activity)
        if form.is_valid():
            messages.error(request, 'FORM VALID')
            activity = form.save(commit=False)
            # problem.author = request.user
            activity.publication_date = timezone.now()
            activity.save()
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
        }
    return render(request, 'activities/activity_edit.html', context)

def activity_list(request):
    if request.user.has_perm("admin_app.change_problem"):
        activities = Activity.objects.all().order_by('title')
    else:
        activities = Activity.objects.filter(publication_status='Published').order_by('title')
    return render(request, 'activities/activity_list.html', {'activities': activities})

def activity_detail(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    # topic_list = activity.topics.strip().rstrip(",").split(",")
    # topic_list = map(str.strip, topic_list)
    # tob = activity.type_of_beast.strip("('")
    # tob = tob.strip("'),")
    this_key = pk
    figures_list = Activity.objects.get(id=this_key).media.all()
    view_name = 'activity_detail'
    form = ActivityFormReadOnly(instance=activity)
    context = {
        'activity': activity,
        # 'tob': tob,
        'this_key': this_key,
        'form': form,
        'view_name': view_name,
        # 'topic_list': topic_list,
        'figures': figures_list
    }
    return render(request, 'activities/activity_detail.html', context)

def activity_detail_solution(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    # topic_list = activity.topics.strip().rstrip(",").split(",")
    # topic_list = map(str.strip, topic_list)
    this_key = pk
    view_name = 'activity_detail_solution'
    form = ActivityFormReadOnly(instance=activity)
    # tob = activity.type_of_beast.strip("('")
    # tob = tob.strip("'),")
    context = {
        'activity': activity,
        # 'tob': tob,
        'this_key': this_key,
        'form': form,
        'view_name': view_name,
        # 'topic_list': topic_list,
    }
    return render(request, 'activities/activity_detail.html', context)
