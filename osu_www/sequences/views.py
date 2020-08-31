#from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.db import IntegrityError, transaction
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.forms.formsets import formset_factory
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils import timezone
from admin_app.models import Sequence, Problem, Activity, SequenceItems
from sequences.forms import SequenceForm, ItemUpdateForm
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.models import Group, User
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from subprocess import Popen, PIPE, STDOUT
import subprocess, os
import unicodedata
import logging
user = get_user_model()

# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)

@permission_required('admin_app.can_edit_sequence',login_url='/')
def sequence_new(request):
    # problem = get_object_or_404(Problem, pk=pk)
    if request.method == "POST":
        # logging.debug('FORM POSTED')
        # messages.error(request, 'ONEONEONE')
        form = SequenceForm(request.POST, request.FILES)
        if form.is_valid():
            # messages.error(request, 'TWOTWOTWO')
            sequence = form.save(commit=False)
            sequence.author = request.user
            sequence.save()
            return redirect('sequence_detail_solution', pk=sequence.pk)
        else:
            messages.error(request, form.errors)
            #return redirect('problem_edit_preview', pk=problem.pk)
    else:
        form = SequenceForm()
    return render(request, 'sequences/sequence_add.html', {'form': form, 'page_title': 'Add Sequence'})

@permission_required('admin_app.can_edit_sequence',login_url='/')
def sequence_edit(request, pk):
    view_name = 'sequence_edit'
    sequence = get_object_or_404(Sequence, pk=pk)

    available_problems = Problem.objects.exclude(id__in = sequence.problems.all().values_list('id'))

    available_activities = Activity.objects.exclude(id__in = sequence.activities.all().values_list('id'))
    thisSequenceID = sequence.pk

    ItemFormSet = formset_factory(ItemUpdateForm, extra=0)

    # item_sql = 'select i.*, a.title, p.problem_title, i.activity_id, i.problem_id, i.sequence_id from admin_app_sequenceitems i LEFT JOIN admin_app_activity a ON i.activity_id = a.id LEFT JOIN admin_app_problem p ON i.problem_id = p.id WHERE i.sequence_id = "' + str(thisSequenceID) + '" ORDER BY i.item_position'

    # print(item_sql)

    # item_list = SequenceItems.objects.raw(item_sql)

    item_list = SequenceItems.objects.filter(sequence=sequence).order_by('item_position')

    # Get list of all associated items
    item_title_sql = 'select i.id, p.problem_title, a.title from admin_app_sequenceitems i LEFT JOIN admin_app_activity a ON i.activity_id = a.id LEFT JOIN admin_app_problem p ON i.problem_id = p.id WHERE i.sequence_id = "' + str(thisSequenceID) + '" ORDER BY i.item_position'

    item_title_list = SequenceItems.objects.raw(item_title_sql)

    item_title_dict = []

    # Loop through them and grab either the activity or problem title and insert it into the title dictionary
    for title in item_title_list:
        if title.title:
            item_title_dict.append( [title.title] )
        else:
            item_title_dict.append( [title.problem_title] )

    # print(item_title_dict)

    # my_key = {"19":"foop", "20":"moop"}
    # print("ITEM LIST:")
    # print(item_list)

    # item_data = [{'item_position': i.item_position, 'role_in_sequence': i.role_in_sequence, 'item_problem_title': i.problem_title, 'item_title': i.title, 'sequence_id': i.sequence_id, 'problem_id': i.problem_id, 'activity_id': i.activity_id}
        # for i in item_list]

    item_data = [{'item_position': i.item_position, 'role_in_sequence': i.role_in_sequence, 'problem': i.problem, 'activity': i.activity, 'sequence': i.sequence, 'required': i.required}
        for i in item_list]

    print("ITEM_DATA:")
    print(item_data)

    if request.method == "POST":
        form = SequenceForm(request.POST, request.FILES, instance=sequence)
        item_formset = ItemFormSet(request.POST)

        if form.is_valid() and item_formset.is_valid():
            # messages.error(request, 'FORM VALID')
            sequence = form.save(commit=False)
            sequence.author = request.user
            sequence.save()

            new_items = []

            for f in item_formset:
                print("STARTING NEW FORMSET ITEM")
                cd = f.cleaned_data
                # print("CD: " + str(cd))
                role_in_sequence = cd.get('role_in_sequence')
                item_position = cd.get('item_position')
                required = cd.get('required')
                # print("REQUIRED: " + required)
                sequence = cd.get('sequence')
                problem = cd.get('problem')
                activity = cd.get('activity')

                # if item_position and role_in_sequence:
                # print("LOADING NEW ITEM INTO ARRAY")
                new_items.append(SequenceItems(item_position=item_position, role_in_sequence=role_in_sequence, sequence=sequence, activity=activity, problem=problem, required=required))
                # print("NEW ITEMS ARRAY: " + str(new_items))

            try:
                with transaction.atomic():
                    # print("DELETING ORIGINAL ITEMS")
                    SequenceItems.objects.filter(sequence_id=thisSequenceID).delete()
                    # print("ADDING NEW ITEMS IN BULK")
                    SequenceItems.objects.bulk_create(new_items)
                    messages.success(request, 'You have updated your sequence.')

            except IntegrityError:
                messages.error(request, 'There was an error updating your sequence')
                # return.redirect(reverse('profile-settings'))
        return redirect('sequence_edit', pk=sequence.pk)

    else:
        form = SequenceForm(instance=sequence)
        item_formset = ItemFormSet(initial=item_data)
        context = {
            'sequence': sequence,
            'problems': available_problems,
            'activities': available_activities,
            'thisSequenceID': thisSequenceID,
            'form': form,
            'view_name': view_name,
            'item_list': item_list,
            # 'item_form': item_form,
            'item_formset': item_formset,
            'item_title_dict': item_title_dict,
            'page_title': sequence.title + ' - Edit',
        }
        return render(request, 'sequences/sequence_edit.html', context)

def sequence_list(request):
    #problems = Problem.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

    if request.user.has_perm("admin_app.change_problem"):
        sequences = Sequence.objects.all().order_by('title')
    else:
        sequences = Sequence.objects.filter(publication=1).order_by('title')
    return render(request, 'sequences/sequence_list.html', {'sequences': sequences, 'page_title': 'Sequences'})

def sequence_title(request, pk):
    sequence = get_object_or_404(Sequence, pk=pk)
    sequence_title = sequence.title
    return HttpResponse(sequence_title)

def sequence_detail(request, pk):
    sequence = get_object_or_404(Sequence, pk=pk)
    thisPrimaryKey = sequence.pk
    item_list_sql = 'select i.id, p.problem_title, a.title, p.problem_latex, a.overview_paragraph, i.role_in_sequence, i.problem_id, i.activity_id, p.publication, a.publication_status from admin_app_sequenceitems i LEFT JOIN admin_app_activity a ON i.activity_id = a.id LEFT JOIN admin_app_problem p ON i.problem_id = p.id WHERE i.sequence_id = "' + str(pk) + '" ORDER BY i.item_position'
    sequence_items = SequenceItems.objects.raw(item_list_sql)
    # logger.error('THISPRIMARYKEY: ' + str(thisPrimaryKey))
    problem_list = Sequence.objects.get(id=thisPrimaryKey).problems.all()
    activity_list = Sequence.objects.get(id=thisPrimaryKey).activities.all()
    form = SequenceForm(instance=sequence)
    view_name = 'sequence_detail'
    # print(sequence.title + "FOO")
    context = {
        'sequence': sequence,
        'problem_list': problem_list,
        'activity_list': activity_list,
        'form': form,
        'view_name': view_name,
        'sequence_items': sequence_items,
        'page_title': sequence.title,
    }
    return render(request, 'sequences/sequence_detail.html', context)

def sequence_detail_solution(request, pk):
    sequence = get_object_or_404(Sequence, pk=pk)
    thisPrimaryKey = sequence.pk
    item_list_sql = 'select i.id, p.problem_title, a.title, p.problem_latex, a.overview_paragraph, i.role_in_sequence, p.publication, a.publication_status from admin_app_sequenceitems i LEFT JOIN admin_app_activity a ON i.activity_id = a.id LEFT JOIN admin_app_problem p ON i.problem_id = p.id WHERE i.sequence_id = "' + str(pk) + '" ORDER BY i.item_position'
    sequence_items = SequenceItems.objects.raw(item_list_sql)
    # sequence_items = SequenceItems.objects.filter(sequence=sequence).order_by('item_position')
    # logger.error('THISPRIMARYKEY: ' + str(thisPrimaryKey))
    problem_list = Sequence.objects.get(id=thisPrimaryKey).problems.all()
    activity_list = Sequence.objects.get(id=thisPrimaryKey).activities.all()
    item_list = SequenceItems.objects.filter(sequence_id=thisPrimaryKey).order_by('item_position')
    form = SequenceForm(instance=sequence)
    view_name = 'sequence_detail_solution'
    context = {
        'sequence': sequence,
        'sequence_items': sequence_items,
        'problem_list': problem_list,
        'activity_list': activity_list,
        'item_list': item_list,
        'form': form,
        'view_name': view_name,
        'page_title': sequence.title + ' - Solutions',
    }
    return render(request, 'sequences/sequence_detail.html', context)

# Associate problem/activity, remove problem/activity
def associate_problem(request, sequence_id, problem_id):
    # messages.error(request, 'ASSOCIATE_PROBLEM BEFORE')
    Sequence.objects.get(id=sequence_id).problems.add(problem_id)
    # messages.error(request, 'ASSOCIATE_PROBLEM AFTER')
    return redirect('sequence_edit', pk=sequence_id)

def associate_activity(request, sequence_id, activity_id):
    Sequence.objects.get(id=sequence_id).activities.add(activity_id)
    return redirect('sequence_edit', pk=sequence_id)

def unassociate_problem(request, sequence_id, problem_id):
    Sequence.objects.get(id=sequence_id).problems.remove(problem_id)
    return redirect('sequence_edit', pk=sequence_id)

def unassociate_activity(request, sequence_id, activity_id):
    Sequence.objects.get(id=sequence_id).activities.remove(activity_id)
    return redirect('sequence_edit', pk=sequence_id)

# @permission_required('admin_app.can_edit_sequence',login_url='/')
# class update_sequence_item(UpdateView):
#     model = SequenceItems
#     fields = ['item_position','role_in_sequence']

# @permission_required('admin_app.can_edit_sequence',login_url='/')
# def update_sequence_item(request, sequence_id, item_id):
#     # problem = get_object_or_404(Problem, pk=pk)
#     sequence_item = SequenceItems.objects.get(id=item_id)
#     if request.method == 'POST':
#         item_form = ItemUpdateForm(request.POST, instance=sequence_item)
#         item_form.save()

    # sequence_item.item_position = '2'
    # sequence_item.role_in_sequence =
    # sequence_item.save()
    # if request.method == "POST":
    #     logging.error('FORM POSTED')
    #     # messages.error(request, 'ONEONEONE')
    #     item_form = ItemUpdateForm(request.POST)
    #     if item_form.is_valid():
    #         messages.error(request, 'TWOTWOTWO')
    #         itemDetails = item_form.save(commit=False)
    #         itemDetails.save()
    #         return redirect('sequence_edit', pk=sequence_id)
    #     else:
    #         messages.error(request, form.errors)
    #         #return redirect('problem_edit_preview', pk=problem.pk)
    # else:
    #     itemForm = ItemUpdateForm()
    # return redirect('sequence_edit', pk=sequence_id)
