from django import forms
from django.conf import settings
from django.core.files.storage import FileSystemStorage, Storage
from django.utils.crypto import get_random_string
from django.conf.urls.static import static
from django.forms import modelformset_factory, inlineformset_factory
from django.forms.formsets import BaseFormSet
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import View
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.models import Group, User
from django.contrib.auth import get_user_model
user = get_user_model()
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from subprocess import Popen, PIPE, STDOUT
import subprocess, os, uuid
import unicodedata
import logging
import datetime

from django.contrib.sites.models import Site
import pdfkit

# import django_filters
from decimal import Decimal

from admin_app.models import ProblemSet, Problem, ProblemSetItems, ProblemSetPDFs

from django.http import FileResponse
# from reportlab.pdfgen import canvas

from django.template.loader import render_to_string

from weasyprint import HTML

def output_pdf(request, problem_set_id):
	current_url = Site.objects.get_current()
	print(current_url)
	pdf = pdfkit.from_url("https://www.google.com", False)
	
	response = HttpResponse(pdf,content_type='application/pdf')
	
	response = HttpResponse['Content-Disposition'] = 'attachment; filename="foo.pdf"'
	
	return response

def output_home(request):
    problem_sets = ProblemSet.objects.all().order_by('title')
    return render(request, 'output/home.html', {'problem_sets': output_problem_set_display})

# A page to display a given problem set layout and initiate the creation of a pdf
def output_problem_set_display(request, problem_set_id):
    # Retrieve the ProblemSet record
    problem_set = ProblemSet.objects.get(pk=problem_set_id)
    page_title = problem_set.title

    # Pass the content to the template for use/rendering
    context = {
        'problem_set': problem_set,
        'page_title': page_title,
        'page_title': problem_set.title,
    }

    return render(request, 'output/problem_set_render.html', context)

# The pdf generation script
def output_problem_set_pdf(request, problem_set_id):

    # Retrieve the ProblemSet record
    problem_set = ProblemSet.objects.get(pk=problem_set_id)
    page_title = problem_set.title

    # Pass the content to the template for use/rendering
    context = {
        'problem_set': problem_set,
        'page_title': page_title,
        'page_title': problem_set.title,
    }

    # Pass the problem set info to template (from weasyprint samples) and render it back to us as a string
    html_string = render_to_string('output/problem_set_render.html', context)

    # Use weasyprint to deal with the html string
    html = HTML(string=html_string)

    # Create a random string to ensure filename is unique
    random_string = "%s.%s" % (get_random_string(length=7), "pdf")

    # Build the filename
    this_file_name = problem_set.title + "_" + random_string

    # Write out the pdf to the actual file
    html.write_pdf(presentational_hints=True, target=settings.MEDIA_ROOT + "/problem_set_pdfs/" + this_file_name)

    # Create a record for this PDF in the InvoicePDF table.
    ProblemSetPDFs.objects.create(problem_set=problem_set, pdf="problem_set_pdfs/" + this_file_name)

    # Define a variable to contain the PDF for serving to user. Serve to user.
    fs = FileSystemStorage(settings.MEDIA_ROOT + "/problem_set_pdfs/")
    with fs.open(this_file_name) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="' + this_file_name + '"'
        return response

    return response
