from django import forms
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.forms import modelformset_factory, inlineformset_factory
from django.forms.formsets import BaseFormSet
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
import logging
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from admin_app.models import ProblemSet, Problem, ProblemSetItems
from problem_sets.forms import ProblemGroupForm, ProblemGroupItemsFormset, ProblemSetForm
# import tkinter as tk
# from tkinter import Tk, BOTH, Menu

# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)

@permission_required('admin_app.can_edit_problem_set',login_url='/')
def problem_set_add(request):
    if request.method == "POST":
        form = ProblemSetForm(request.POST)
        if form.is_valid():
            # messages.error(request, 'TWOTWOTWO')
            problem_set = form.save(commit=False)
            problem_set.author = request.user
            problem_set.save()
            return redirect('edit_problem_set', problem_set_id=problem_set.pk)
        else:
            messages.error(request, form.errors)
            #return redirect('problem_edit_preview', pk=problem.pk)
    else:
        form = ProblemSetForm()
    return render(request, 'problem_sets/problem_set_add.html', {'form': form})


@permission_required('admin_app.can_edit_problem_set',login_url='/')
def problem_set_details_solution(request, problem_set_id):
    problem_set = ProblemSet.objects.get(pk=problem_set_id)
    problem_set_items = ProblemSetItems.objects.filter(problem_set_id=problem_set_id)
    problem_set_problems = ProblemSetItems.objects.select_related().filter(problem_set_id=problem_set.pk)

    # print(problem_set_items)
    # print(problem_set_problems)

    context = {
        'problem_set': problem_set,
        'problem_set_items': problem_set_items,
        'problem_set_problems': problem_set_problems,
    }

    return render(request, 'problem_sets/problem_set_detail.html', context)

########################### EDIT PROBLEM SET ##################################

@permission_required('admin_app.can_edit_problem_set',login_url='/')
def edit_problem_set(request, problem_set_id):

    problem_group = ProblemSet.objects.get(pk=problem_set_id)

    problem_group_form = ProblemGroupForm(instance=problem_group)

    ProblemFormset = inlineformset_factory(
        ProblemSet, ProblemSetItems,
        fields=('item_position','problem','item_instructions',),
        can_delete=True,
        widgets={
            'item_instructions': forms.Textarea(attrs={'cols': 80, 'rows': 2, 'class': 'testclass'}),
            # 'problem': forms.
            },
        formset=ProblemGroupItemsFormset,
        extra=1)

    ProblemFormset2 = inlineformset_factory(
        ProblemSet, ProblemSetItems,
        fields=('item_position','problem','item_instructions',),
        can_delete=True,
        widgets={
            'item_instructions': forms.Textarea(attrs={'cols': 80, 'rows': 2, 'class': 'testclass'}),
            # 'problem': forms.
            },
        formset=ProblemGroupItemsFormset,
        extra=1)

    if request.method == 'POST':

        problem_group_form = ProblemGroupForm(request.POST, instance=problem_group)

        problem_group_item_form = ProblemFormset2(request.POST, instance=problem_group, queryset=problem_group.problemsetitems_set.order_by("item_position"))

        if problem_group_item_form.is_valid() and problem_group_form.is_valid():
            problem_group_item_form.save()

            problem_group_form.save()
            return redirect('edit_problem_set', problem_set_id=problem_group.id)

    # problem_set_item_form = ProblemFormset(instance=problem_set)
    problem_group_item_form = ProblemFormset2(instance=problem_group, queryset=problem_group.problemsetitems_set.order_by("item_position"))

    # for n in problem_group_item_form:
    #     n.fields['problem'].queryset = Menu.objects.filter(problem=problem).order_by('problem')

    context = {
        'formset': problem_group_item_form,
        'problem_group': problem_group,
        'problem_group_form': problem_group_form,
        'problem_set_id': problem_set_id,
    }
    return render(request, 'problem_sets/problem_set_edit.html', context)

@permission_required('admin_app.can_edit_problem_set',login_url='/')
def list_problem_sets(request):
    problem_set_list = ProblemSet.objects.all().order_by('title')
    # print(problem_set_list)
    context = {
        'problem_set_list': problem_set_list,
    }
    return render(request, 'problem_sets/problem_set_list.html', context)

@permission_required('admin_app.can_edit_problem_set',login_url='/')
def problem_set_details(request, problem_set_id):
    problem_set = ProblemSet.objects.get(pk=problem_set_id)
    problem_set_items = ProblemSetItems.objects.filter(problem_set_id=problem_set_id)
    problem_set_problems = ProblemSetItems.objects.select_related().filter(problem_set_id=problem_set.pk)
    # print(problem_set_problems)
    context = {
        'problem_set': problem_set,
        'problem_set_items': problem_set_items,
        'problem_set_problems': problem_set_problems,
    }
    return render(request, 'problem_sets/problem_set_detail.html', context)
