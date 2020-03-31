from django import forms
from django.conf import settings
from django.core.files.storage import FileSystemStorage, Storage
from django.utils.crypto import get_random_string
from django.conf.urls.static import static
from django.forms import modelformset_factory, inlineformset_factory
from django.forms.formsets import BaseFormSet
from django.http import HttpResponse, HttpRequest
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
import re
import socket

from django.contrib.sites.models import Site
import pdfkit

# import django_filters
from decimal import Decimal

from admin_app.models import ProblemSet, Problem, ProblemSetItems, ProblemSetPDFs

from django.http import FileResponse
# from reportlab.pdfgen import canvas

from django.template.loader import render_to_string

from weasyprint import HTML

HTML_WHITESPACE = ' \t\n\f\r'

def strip_whitespace(string):
    """Use the HTML definition of "space character",
    not all Unicode Whitespace.

    http://www.whatwg.org/html#strip-leading-and-trailing-whitespace
    http://www.whatwg.org/html#space-character

    """
    return string.strip(HTML_WHITESPACE)


def output_problem_set_pdf(request, problem_set_id):

	# Find the problem set. We need the title.
	problem_set = ProblemSet.objects.get(pk=problem_set_id)

	# wkhtml needs some options. The most critical is the javascript delay.
	# This is needed to give mathjax a chance to render before the pdf is created
	wkoptions = {
		'javascript-delay': 5000, # 5000 = 5 sec
		'margin-top': '1in',
		'margin-right': '1in',
		'margin-bottom': '1in',
	 	'margin-left': '1in',
		'encoding': "UTF-8",
		# 'load-media-error-handling': 'ignore',
	}

	# Pdfkit requires a url, so we'll build one using what we know about this request
	current_domain = str(Site.objects.get_current())

	try:
		current_domain = request.META['HTTP_HOST']
	except:
		current_domain = 'localhost'

	print("CURRENT DOMAIN: " + str(current_domain))

	if request.is_secure():
		# template_url = 'https://' + current_domain + ':' + request.META['SERVER_PORT'] + '/output/problem_set/display/' + problem_set_id + '/'
		# template_url2 = 'https://' + current_domain + ':' + request.META['SERVER_PORT'] + '/output/problem_set/display_solution/' + problem_set_id + '/'

		template_url = 'https://paradigms.oregonstate.edu/output/problem_set/display/' + problem_set_id + '/'
		template_url2 = 'https://paradigms.oregonstate.edu/output/problem_set/display_solution/' + problem_set_id + '/'

		# print("TEMPLATE S URL: " + str(template_url))

	else:
		template_url = 'http://' + current_domain + ':' + request.META['SERVER_PORT'] + '/output/problem_set/display/' + problem_set_id + '/'
		template_url2 = 'http://' + current_domain + ':' + request.META['SERVER_PORT'] + '/output/problem_set/display_solution/' + problem_set_id + '/'

		template_url = current_domain + '/output/problem_set/display/' + problem_set_id + '/'
		template_url2 = current_domain + '/output/problem_set/display_solution/' + problem_set_id + '/'

		# print("TEMPLATE URL: " + str(template_url))

	# Create a new filename using random string and problem_set title
	random_string = "%s.%s" % (get_random_string(length=7), "pdf")
	random_string2 = "%s.%s" % (get_random_string(length=7), "pdf")
	# print("RANDOM STRINGS: " + random_string + " " + random_string2)

	stripped_title = re.sub(r'\W+', '', problem_set.title)

	# Build the filename
	this_file_name = stripped_title + "_" + random_string
	this_file_name2 = stripped_title + "_" + random_string2

	# print("STRIPPED FILE NAME: " + this_file_name)

	# DIfferent pathing is required based on whether we're working in development or production environments.
	if request.is_secure():
		this_file_path = "/var/www/osu_production_env/osu_www/media/problem_set_pdfs/" + this_file_name
		this_file_path2 = "/var/www/osu_production_env/osu_www/media/problem_set_pdfs/" + this_file_name2
	else:
		this_file_path = "media/problem_set_pdfs/" + this_file_name
		this_file_path2 = "media/problem_set_pdfs/" + this_file_name2

	# print("THIS FILE PATH: " + this_file_path)
	# Create the pdf using the url specified
	pdf = pdfkit.from_url(template_url, this_file_path, options=wkoptions)
	pdf2 = pdfkit.from_url(template_url2, this_file_path2, options=wkoptions)

	# Create a record for this PDF in the InvoicePDF table.
	ProblemSetPDFs.objects.create(problem_set=problem_set, solution=False, pdf="problem_set_pdfs/" + this_file_name)
	ProblemSetPDFs.objects.create(problem_set=problem_set, solution=True, pdf="problem_set_pdfs/" + this_file_name2)

	# Define a variable to contain the PDF for serving to user. Serve to user.
	# fs = FileSystemStorage(settings.MEDIA_ROOT + "/problem_set_pdfs/")
	# with fs.open(this_file_name) as pdf:
	#	response = HttpResponse(pdf, content_type='application/pdf')
	#	response['Content-Disposition'] = 'attachment; filename="' + this_file_name + '"'
	#	return response

	# return response

	# Assuming that this request is coming from the edit problem set page... return there.
	return redirect('edit_problem_set', problem_set_id=problem_set.id)

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
		'solution': 'no',
    }

    return render(request, 'output/problem_set_render.html', context)

def output_problem_set_display_solution(request, problem_set_id):
    # Retrieve the ProblemSet record
    problem_set = ProblemSet.objects.get(pk=problem_set_id)
    page_title = problem_set.title

    # Pass the content to the template for use/rendering
    context = {
        'problem_set': problem_set,
        'page_title': page_title,
        'page_title': problem_set.title,
		'solution': 'yes',
    }

    return render(request, 'output/problem_set_render.html', context)
