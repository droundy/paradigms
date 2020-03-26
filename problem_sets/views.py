from django import forms
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.forms import modelformset_factory, inlineformset_factory
from django.forms.formsets import formset_factory
from django.forms.formsets import BaseFormSet
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
import logging
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from admin_app.models import ProblemSet, Problem, ProblemSetItems, ProblemSetPDFs
from problem_sets.forms import ProblemSetEditForm, ProblemSetItemsFormset, ProblemSetAddForm, SetItemUpdateForm

HTML_WHITESPACE = ' \t\n\f\r'

def strip_whitespace(string):
    """Use the HTML definition of "space character",
    not all Unicode Whitespace.

    http://www.whatwg.org/html#strip-leading-and-trailing-whitespace
    http://www.whatwg.org/html#space-character

    """
    return string.strip(HTML_WHITESPACE)

# import tkinter as tk
# from tkinter import Tk, BOTH, Menu

# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)

@permission_required('admin_app.can_edit_problem_set',login_url='/')
def problem_set_add(request):
    if request.method == "POST":
        form = ProblemSetAddForm(request.POST)
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
        form = ProblemSetAddForm()
    return render(request, 'problem_sets/problem_set_add.html', {'form': form, 'page_title': 'Add Problem Set'})


@permission_required('admin_app.can_edit_problem_set',login_url='/')
def problem_set_details_solution(request, problem_set_id):
    problem_set = ProblemSet.objects.get(pk=problem_set_id)
    problem_set_items = ProblemSetItems.objects.filter(problem_set_id=problem_set_id)
    problem_set_problems = ProblemSetItems.objects.select_related().filter(problem_set_id=problem_set.pk).order_by("item_position")
    page_title = problem_set.title
    problem_set_pdf_solution = ProblemSetPDFs.objects.filter(problem_set_id=problem_set_id).filter(solution=True).order_by('-id')[:1]
    problem_set_pdf = ProblemSetPDFs.objects.filter(problem_set_id=problem_set_id).filter(solution=False).order_by('-id')[:1]

    # print(page_title)
    # print(problem_set_problems)

    context = {
        'problem_set': problem_set,
        'problem_set_items': problem_set_items,
        'problem_set_problems': problem_set_problems,
        'problem_set_pdf': problem_set_pdf,
        'problem_set_pdf_solution': problem_set_pdf_solution,
        'page_title': page_title + ' - Solutions',
    }

    return render(request, 'problem_sets/problem_set_detail.html', context)

########################### EDIT PROBLEM SET ##################################

@permission_required('admin_app.can_edit_problem_set',login_url='/')
def edit_problem_set(request, problem_set_id):

    problem_group = ProblemSet.objects.get(pk=problem_set_id)

    problem_group_form = ProblemSetEditForm(instance=problem_group)

    ProblemFormset = inlineformset_factory(
        ProblemSet, ProblemSetItems,
        fields=('item_position','problem','item_instructions',),
        can_delete=True,
        widgets={
            'item_instructions': forms.Textarea(attrs={'cols': 80, 'rows': 2, 'class': 'testclass'}),
            # 'problem': forms.
            },
        formset=ProblemSetItemsFormset,
        extra=5)

    ProblemFormset2 = inlineformset_factory(
        ProblemSet, ProblemSetItems,
        fields=('item_position','problem','item_instructions',),
        can_delete=True,
        widgets={
            'item_instructions': forms.Textarea(attrs={'cols': 80, 'rows': 2, 'class': 'testclass'}),
            # 'problem': forms.
            },
        formset=ProblemSetItemsFormset,
        extra=5)

    if request.method == 'POST':

        data = request.POST.copy()

        # Handle a comma-delimited list of problem ids to be added to this list
        if data.get('bulk_item_list'):

            print('BULK ITEM LIST FOUND ' + data.get('bulk_item_list'))

            #  Find the highest number in this sequence so far. May be zero, null, or empty
            highest_position_record = ProblemSetItems.objects.select_related().filter(problem_set_id=problem_set_id).order_by("-item_position").first()

            #  We found an existing record, set the highest position variable
            if highest_position_record:
                print("HIGEST POSITION RECORD: " + str(highest_position_record) + '---' + str(highest_position_record.item_position))
                highestPosition = highest_position_record.item_position
            else:
                # This problem set has no items so far. Set a default high position.
                highestPosition = 0

            print("HIGHEST POSITION: " + str(highestPosition))

            # Set up a counter to increment the positions for new problems in this set
            if highestPosition:
                counter = highestPosition + 1
            else:
                counter = 0

            # Take the input and clean it up, filtering for whitespace and non-numeric entries
            for problemID in map(strip_whitespace, data.get('bulk_item_list').split(',')):

                #  Is this a digit?
                if problemID.isdigit():

                    # Display the problem id
                    print("PROBLEM ID: " + problemID)

                    # Determine if this problem exists or not
                    try:
                        thisProblem = Problem.objects.get(id=problemID)
                        print("THIS PROBLEM RESULT: " + str(thisProblem))
                        # Problem found, add it to the problem set items

                        # But first, check to see if this problem exists in this set.
                        itemTest = ProblemSetItems.objects.select_related().filter(problem_set_id=problem_set_id).filter(problem_id=problemID).first()

                        print(itemTest)

                        if itemTest:
                            print("Item Already Exists in this Problem Set")
                        else:
                            newItem = ProblemSetItems(item_position=counter, problem_set_id=problem_set_id, problem_id=problemID)

                            newItem.save()

                            # Increase the counter
                            counter = counter + 1

                    except Problem.DoesNotExist:
                        print("PROBLEM NOT FOUND")
                        # If the problem does not exist do not add it, pause process, warn user
                        # Or fail silently.

                else:
                    print("NOT AN INTEGER")

            return redirect('edit_problem_set', problem_set_id=problem_group.id)

        # Handle problems using the inline formset
        else:

            problem_group_form = ProblemSetEditForm(request.POST, instance=problem_group)

            problem_group_item_form = ProblemFormset2(request.POST, instance=problem_group, queryset=problem_group.set_problems.order_by("item_position"))

            if problem_group_item_form.is_valid() and problem_group_form.is_valid():
                problem_group_item_form.save()

                problem_group_form.save()

                return redirect('edit_problem_set', problem_set_id=problem_group.id)

    # problem_set_item_form = ProblemFormset(instance=problem_set)
    # problem_group_item_form = ProblemFormset2(instance=problem_group, queryset=problem_group.set_problems.order_by("item_position"))

    problem_group_item_form = ProblemFormset2(instance=problem_group, queryset=problem_group.set_problems.order_by("item_position"))

    # for n in problem_group_item_form:
    #     n.fields['problem'].queryset = Menu.objects.filter(problem=problem).order_by('problem')

    context = {
        'formset': problem_group_item_form,
        'problem_group': problem_group,
        'problem_group_form': problem_group_form,
        'problem_set_id': problem_set_id,
        'page_title': problem_group.title + ' - Edit',
    }
    return render(request, 'problem_sets/problem_set_edit.html', context)


@permission_required('admin_app.can_edit_problem_set',login_url='/')
def edit_problem_set_3(request, problem_set_id):

    problem_group = ProblemSet.objects.get(pk=problem_set_id)

    problem_set = problem_group

    available_problems = Problem.objects.exclude(id__in = problem_group.set_problems.all().values_list('id').order_by('problem_title'))

    problem_group_form = ProblemSetEditForm(instance=problem_group)

    ProblemFormset = inlineformset_factory(
        ProblemSet, ProblemSetItems,
        fields=('problem','item_position','item_instructions','required'),
        can_delete=True,
        widgets={
            'item_instructions': forms.Textarea(attrs={'cols': 80, 'rows': 2, 'class': 'testclass'}),
            # 'problem': forms.
            },
        formset=ProblemSetItemsFormset,
        extra=0)

    ProblemFormset2 = inlineformset_factory(
        ProblemSet, ProblemSetItems,
        fields=('problem','item_position','item_instructions','required'),
        can_delete=True,
        widgets={
            'item_instructions': forms.Textarea(attrs={'cols': 80, 'rows': 2, 'class': 'testclass'}),
            # 'problem': forms.
            },
        formset=ProblemSetItemsFormset,
        extra=0)

    # Get list of all associated items
    item_title_sql = 'select i.id, p.problem_title from admin_app_problemsetitems i LEFT JOIN admin_app_problem p ON i.problem_id = p.id WHERE i.problem_set_id = "' + str(problem_set_id) + '" ORDER BY i.item_position'

    item_title_list = ProblemSetItems.objects.raw(item_title_sql)

    item_title_dict = []

    # Loop through them and grab either the activity or problem title and insert it into the title dictionary
    for title in item_title_list:
        item_title_dict.append( [title.problem_title] )

    if request.method == 'POST':

        data = request.POST.copy()

        # Handle a comma-delimited list of problem ids to be added to this list
        if data.get('bulk_item_list'):

            print('BULK ITEM LIST FOUND ' + data.get('bulk_item_list'))

            #  Find the highest number in this sequence so far. May be zero, null, or empty
            highest_position_record = ProblemSetItems.objects.select_related().filter(problem_set_id=problem_set_id).order_by("-item_position").first()

            #  We found an existing record, set the highest position variable
            if highest_position_record:
                print("HIGEST POSITION RECORD: " + str(highest_position_record) + '---' + str(highest_position_record.item_position))
                highestPosition = highest_position_record.item_position
            else:
                # This problem set has no items so far. Set a default high position.
                highestPosition = 0

            print("HIGHEST POSITION: " + str(highestPosition))

            # Set up a counter to increment the positions for new problems in this set
            if highestPosition:
                counter = highestPosition + 1
            else:
                counter = 0

            # Take the input and clean it up, filtering for whitespace and non-numeric entries
            for problemID in map(strip_whitespace, data.get('bulk_item_list').split(',')):

                #  Is this a digit?
                if problemID.isdigit():

                    # Display the problem id
                    print("PROBLEM ID: " + problemID)

                    # Determine if this problem exists or not
                    try:
                        thisProblem = Problem.objects.get(id=problemID)
                        print("THIS PROBLEM RESULT: " + str(thisProblem))
                        # Problem found, add it to the problem set items

                        # But first, check to see if this problem exists in this set.
                        itemTest = ProblemSetItems.objects.select_related().filter(problem_set_id=problem_set_id).filter(problem_id=problemID).first()

                        print(itemTest)

                        if itemTest:
                            print("Item Already Exists in this Problem Set")
                        else:
                            newItem = ProblemSetItems(item_position=counter, problem_set_id=problem_set_id, problem_id=problemID)

                            newItem.save()

                            # Increase the counter
                            counter = counter + 1

                    except Problem.DoesNotExist:
                        print("PROBLEM NOT FOUND")
                        # If the problem does not exist do not add it, pause process, warn user
                        # Or fail silently.

                else:
                    print("NOT AN INTEGER")

            return redirect('edit_problem_set', problem_set_id=problem_group.id)

        # Handle problems using the inline formset
        else:

            problem_group_form = ProblemSetEditForm(request.POST, instance=problem_group)

            problem_group_item_form = ProblemFormset2(request.POST, instance=problem_group, queryset=problem_group.set_problems.order_by("item_position"))

            if problem_group_item_form.is_valid() and problem_group_form.is_valid():
                problem_group_item_form.save()

                problem_group_form.save()

                return redirect('edit_problem_set', problem_set_id=problem_group.id)

    # problem_set_item_form = ProblemFormset(instance=problem_set)
    # problem_group_item_form = ProblemFormset2(instance=problem_group, queryset=problem_group.set_problems.order_by("item_position"))

    problem_group_item_form = ProblemFormset2(instance=problem_group, queryset=problem_group.set_problems.order_by("item_position"))

    # for n in problem_group_item_form:
    #     n.fields['problem'].queryset = Menu.objects.filter(problem=problem).order_by('problem')

    context = {
        'formset': problem_group_item_form,
        'problems': available_problems,
        'problem_group': problem_group,
        'problem_set': problem_set,
        'problem_group_form': problem_group_form,
        'item_title_dict': item_title_dict,
        'problem_set_id': problem_set_id,
        'page_title': problem_group.title + ' - Edit',
    }
    return render(request, 'problem_sets/problem_set_edit_3.html', context)
# @permission_required('admin_app.can_edit_problem_set',login_url='/')
# def edit_problem_set_2(request, problem_set_id):
#     # Find the problem set details
#     problem_set = ProblemSet.objects.get(pk=problem_set_id)
#
#     problem_set_form = ProblemSetEditForm(instance=problem_set)
#
#     ProblemsFormset = inlineformset_factory(
#         ProblemSet, ProblemSetItems,
#         fields=('item_position','problem','item_instructions',),
#         can_delete=True,
#         widgets={
#             'item_instructions': forms.Textarea(attrs={'cols': 80, 'rows': 2, 'class': 'testclass'}),
#             # 'problem': forms.
#             },
#         extra=5,
#         formset=ProblemSetItemsFormset,
#     )
#
#     problem_set_item_form = ProblemsFormset(instance=problem_set, queryset=problem_set.set_problems.order_by("item_position"))
#
#     context = {
#         'formset': problem_set_item_form,
#         'problem_set': problem_set,
#         'problem_set_form': problem_set_form,
#         'problem_set_id': problem_set_id,
#         'page_title': problem_set.title + ' - Edit',
#     }
#     return render(request, 'problem_sets/problem_set_edit_2.html', context)

# Make it more like editing a Sequence of activities.

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
    problem_set_problems = ProblemSetItems.objects.select_related().filter(problem_set_id=problem_set.pk).order_by("item_position")
    problem_set_pdf_solution = ProblemSetPDFs.objects.filter(problem_set_id=problem_set_id).filter(solution=True).order_by('-id')[:1]
    problem_set_pdf = ProblemSetPDFs.objects.filter(problem_set_id=problem_set_id).filter(solution=False).order_by('-id')[:1]
    # print(problem_set_problems)
    context = {
        'problem_set': problem_set,
        'problem_set_items': problem_set_items,
        'problem_set_problems': problem_set_problems,
        'problem_set_pdf': problem_set_pdf,
        'problem_set_pdf_solution': problem_set_pdf_solution,
        'page_title': problem_set.title,
    }
    return render(request, 'problem_sets/problem_set_detail.html', context)

# Associate problem/activity, remove problem/activity
def associate_problem_to_set(request, problem_set_id, problem_id):
    ProblemSet.objects.get(id=problem_set_id).items.add(problem_id)
    return redirect('edit_problem_set_3', problem_set_id=problem_set_id)


def unassociate_problem_from_set(request, problem_set_id, problem_id):
    problem = Problem.objects.get(id=problem_id)
    ProblemSet.objects.get(id=problem_set_id).items.remove(problem_id)
    return redirect('edit_problem_set_3', problem_set_id=problem_set_id)
