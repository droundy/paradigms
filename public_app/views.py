#from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from admin_app.models import Problem, Figure, FigureAssociations
from public_app.forms import ProblemForm
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.models import Group, User, Permission
from django.contrib.auth import get_user_model
user = get_user_model()
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from subprocess import Popen, PIPE, STDOUT
import subprocess, os
import unicodedata
import logging

# @permission_required('admin_app.can_edit_problem',login_url='/')
def problem_list(request):
    if request.user.has_perm("admin_app.can_edit_problem"):
        problems = Problem.objects.all().order_by('problem_title')
    else:
        problems = Problem.objects.filter(publication=1).order_by('problem_title')
    return render(request, 'public_app/problem_list.html', {'problems': problems, 'page_title': 'Homework Problems'})

@permission_required('admin_app.can_add_problem',login_url='/')
def problem_new(request):
    # problem = get_object_or_404(Problem, pk=pk)
    if request.method == "POST":
        # logging.debug('request.method=POST')
        # messages.error(request, 'ONEONEONE')
        form = ProblemForm(request.POST)
        if form.is_valid():
            # messages.error(request, 'TWOTWOTWO')
            problem = form.save(commit=False)
            # problem.author = request.user
            problem.published_date = timezone.now()
            problem.save()
            return redirect('problem_edit_preview', pk=problem.pk)
        else:
            messages.error(request, form.errors)
            #return redirect('problem_edit_preview', pk=problem.pk)
    else:
        form = ProblemForm()
    return render(request, 'public_app/problem_multi_edit_preview.html', {'form': form, 'page_title': 'Add Homework Problem'})

#@login_required
@permission_required('admin_app.can_edit_problem',login_url='/')
def problem_edit(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    if request.method == "POST":
        form = ProblemForm(request.POST, instance=problem)
        if form.is_valid():
            problem = form.save(commit=False)
            # problem.author = request.user
            problem.published_date = timezone.now()
            problem.save()
            return redirect('problem_display_html', pk=problem.pk)
    else:
        form = ProblemForm(instance=problem)
    return render(request, 'public_app/problem_edit.html', {'form': form, 'testVar': 'TEST VAR THING', 'page_title': problem.problem_title + ' - Edit'})

####
#@login_required
@permission_required('admin_app.can_edit_problem',login_url='/')
def problem_edit_preview(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    if request.method == "POST":
        form = ProblemForm(request.POST, instance=problem)
        if form.is_valid():
            problem = form.save(commit=False)
            # problem.author = request.user
            problem.published_date = timezone.now()
            problem.save()
            return redirect('problem_edit_preview', pk=problem.pk)
        else:
            messages.error(request, form.errors)
            #return redirect('problem_edit_preview', pk=problem.pk)
    else:
        form = ProblemForm(instance=problem)
        thisPrimaryKey = problem.pk
        figures_list = Problem.objects.get(id=thisPrimaryKey).figures.all()
        context = {
            'thisPrimaryKey' : thisPrimaryKey,
            'form' : form,
            'figures': figures_list,
            'latex_problem': problem,
            'page_title': problem.problem_title + ' - Edit',
        }
    return render(request, 'public_app/problem_multi_edit_preview.html', context)

####


def sequences(request):
    return render(request, 'public_app/sequences.html', {})

def index(request):
    #return HttpResponse("This is the home page")
    return render(request, 'public_app/index.html', {})

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROBLEM_SCRIPT = os.path.join(BASE_DIR, 'shell_scripts/homework_archive/problem')

def get_problem_html(ppk):
    command = [PROBLEM_SCRIPT,"--latex","--pk",ppk]
    try:
        process = Popen(command, stdout=PIPE, stderr=STDOUT)
        output = process.stdout.read()
        exitstatus = process.poll()
        if (exitstatus==0):
            return str(output.decode('utf-8'))
        else:
            return {"status": "Failed", "output":str(output)}
    except Exception as e:
        return {"status": "failed", "output":str(e)}

def get_problem_html_solution(ppk):
    command = [PROBLEM_SCRIPT,"--latex","--pk","--solution",ppk]
    try:
        process = Popen(command, stdout=PIPE, stderr=STDOUT)
        output = process.stdout.read()
        exitstatus = process.poll()
        if (exitstatus==0):
            return str(output.decode('utf-8'))
        else:
            return {"status": "Failed", "output":str(output)}
    except Exception as e:
        return {"status": "failed", "output":str(e)}

def get_problem_pdf():
    command = [PROBLEM_SCRIPT,"--pdf","--pk","1"]
    try:
        process = Popen(command, stdout=PIPE, stderr=STDOUT)
        output = process.stdout.read()
        exitstatus = process.poll()
        if (exitstatus==0):
            return {"status": "Success", "output":str(output)}
        else:
            return {"status": "Failed", "output":str(output)}
    except Exception as e:
        return {"status": "failed", "output":str(e)}

# For display within site layout.
#@csrf_exempt
@permission_required('admin_app.can_edit_problem')
def problem_display_html_solution(request, pk):
    latex_problem = get_object_or_404(Problem, pk=pk)
    data = get_problem_html_solution(str(pk))
    # this_key = request.path.split("/")[-1]
    this_key = pk
    figures_list = Problem.objects.get(id=this_key).figures.all()
    # print(this_key)
    context = {
        'page_problem': data,
        'latex_problem': latex_problem,
        'this_key' : this_key,
        'figures': figures_list,
        'page_title': latex_problem.problem_title + ' - Solution',
    }
    return render(request, 'public_app/problem_display.html', context)

# @permission_required('admin_app.can_edit_problem',login_url='/')
def problem_display_html(request, pk):
    latex_problem = get_object_or_404(Problem, pk=pk)
    if latex_problem.publication == 1 or request.user.has_perm("admin_app.change_problem"):
        data = get_problem_html(str(pk))
        # this_key = URL.split("/")[-1]
        this_key = pk
        figures_list = Problem.objects.get(id=this_key).figures.all()
        # print(this_key)
        # print(data)
        context = {
            'page_problem': data,
            'latex_problem': latex_problem,
            'this_key' : this_key,
            'figures': figures_list,
            'page_title': latex_problem.problem_title,
        }
        return render(request, 'public_app/problem_display.html', context)
    else:
        return redirect('/accounts/login/?next=%s' % request.path)


def problem_title(request, pk):
    activity = get_object_or_404(Problem, pk=pk)
    problem_title = problem.title
    return HttpResponse(problem_title)

# For display within site layout.
#@csrf_exempt

def problem_display_pdf(request, pk):
    data = get_problem_pdf
    response = HttpResponse(data, content_type='application/pdf', status=200)
    return response

@csrf_exempt
def problem_render_html(request, pk):
    latex_problem = get_object_or_404(Problem, pk=pk)
    data = get_problem_html(str(pk))
    context = {
        'page_problem': data,
        'latex_problem': latex_problem
    }
    response = HttpResponse(data, content_type='text/plain; charset=utf-8', status=200)
    return response

# For rendering html from raw posted latex rather than latex from database record with primary key
# For use only with ajax calls sending the latex content as a post variable named problem_latex

def get_problem_html_no_pk(latex_problem):
    command = [PROBLEM_SCRIPT,"--html","--solution"]
    try:
        status = subprocess.run(command, input=latex_problem.encode('utf-8'), stdout=PIPE, stderr=STDOUT)
        if status.returncode==0:
            return status.stdout.decode('utf-8')
        else:
            return {"status": "Failed", "output":str(output)}
    except Exception as e:
        return {"status": "failed", "output":str(e)}

@csrf_exempt
def problem_render_raw_html(request):
    problem_latex = request.POST.get('problem_latex')
    data = get_problem_html_no_pk(problem_latex)
    response = HttpResponse(data, content_type='text/plain; charset=utf-8', status=200)
    # response = HttpResponse(problem_latex, content_type='text/plain; charset=utf-8', status=200)
    return response
