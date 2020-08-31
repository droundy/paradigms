import time
import logging
import subprocess, os
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import resolve, include, path
from django.views import View

from .forms import FigureForm
from admin_app.choices import *
from admin_app.models import Figure, Problem, FigureAssociations

# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)

class BasicUploadView(View):

    def get(self, request, problem_id):
        figures_list = Figure.objects.all()
        return render(self.request, 'figures/basic_upload/index.html', {'figures': figures_list})

    def post(self, request):
        form = FigureForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            figure = form.save()
            data = {'is_valid': True, 'name': figure.file.name, 'url': figure.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)

# def BasicUploadView(request, problem_id):
#     def __init__(self, problem_id=problem_id):
#         super().__init__()
#         self.problem_id = problem_id
#     if request.method == "POST":
#         form = FigureForm(self.request.POST, self.request.FILES)
#         problem = Problem.objects.get(id=problem_id)
#         figures_list = FigureAssociations.objects.get(problem_id=problem_id)
#         if form.is_valid():
#             logging.debug('FORM.SAVED BUV1')
#             figure = form.save()
#             data = {'is_valid': True, 'name': figure.file.name, 'url': figure.file.url}
#         else:
#             data = {'is_valid': False}
#             logging.debug('FORM.SAVED BUV2')
#         logging.debug('FORM.SAVED BUV3')
#         return JsonResponse(data)
#     else:
#         figures_list = Figure.objects.all()
#         logging.debug('FORM.SAVED BUV4')
#         return render(self.request, 'figures/basic_upload/index.html', {'figures': figures_list})


# def ProgressBarUploadView(request, problem_id):
#     problem = Problem.objects.get(id=problem_id)
#     figures_list = FigureAssociations.objects.get(problem_id=problem_id)
    # figures_list = Figures.objects.get()
    # problemFigures = FigureAssociations.objects.get(problem_id=problem_id)
    # find unassigned figures?
    # unassigned_figures = Figure.objects.exclude(id__in = problem.figures.all().values_list('id'))

class ProgressBarUploadView(View):
    def get(self, request, problem_id):
        # retrieve list of figures for this specific problem
        latex_problem = get_object_or_404(Problem, pk=problem_id)
        figures_list = Problem.objects.get(id=problem_id).figures.all()
        thisProblemID = latex_problem.pk
        media_categories = MEDIATYPECHOICES
        context = {
            'thisProblemID': thisProblemID,
            'figures': figures_list,
            'latex_problem': latex_problem,
            'media_categories': media_categories,
            'page_title': latex_problem.problem_title + ' - Figures',
        }
        return render(self.request, 'figures/progress_bar_upload/index.html', context)

    def post(self, request, *args, **kwargs):
        time.sleep(1)  # You don't need this line. This is just to delay the process so you can see the progress bar testing locally.
        form = FigureForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            logger.error("YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY")
            # logger.error(str(request.path))
            logger.error(str(self.request.POST))

            thisOriginPath = self.request.POST["origin_path"]

            logger.error('ORIGIN_PATH: ' + thisOriginPath)

            thisProblemID = os.path.basename(os.path.normpath(thisOriginPath))

            # thisProblemID = thisOriginPath.split('/')[-1]

            logger.error('PROBLEM_ID: ' + thisProblemID)

            logger.error('FORM: %s ', form)

            if form.is_valid():
                logger.error('FORM IS VALID')
                logger.error('FORM ERRORS: ')
                figure = form.save()
            else:
                logger.error('FORM IS NOT VALID')


            logger.error('AFTER FORM.SAVE FOR FIGURE')

            thisFigureID = figure.pk
            logger.error('FIGURE ID: ' + str(thisFigureID))

            Problem.objects.get(id=int(thisProblemID)).figures.add(int(thisFigureID))
            # return redirect('detail', cat_id=cat_id)

            # thisProblemID = FigureAssociations.objects.get()
            data = {'is_valid': True, 'name': figure.file.name, 'url': figure.file.url, 'newFigureID': thisFigureID}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


class DragAndDropUploadView(View):
    def get(self, request):
        figures_list = Figure.objects.all()
        return render(self.request, 'figures/drag_and_drop_upload/index.html', {'figures': figures_list})

    def post(self, request):
        form = FigureForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            figure = form.save()
            data = {'is_valid': True, 'name': figure.file.name, 'url': figure.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


def delete_figures_for_problem(request, problem_id):
    for fa in Problem.objects.get(id=problem_id).figures.all():
        logger.error(fa)
        fa.file.delete()
        fa.delete()

    # for figure in Figure.objects.all():
    #     figure.file.delete()
    #     figure.delete()
    return redirect(request.POST.get('next'))

def delete_figure(request, figure_id):
    fig = Figure.objects.get(pk=figure_id)
    fig.delete()
    # return redirect(request.POST.get('next'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def delete_all_figures(request):
    for figure in Figure.objects.all():
        figure.file.delete()
        figure.delete()
    return redirect(request.POST.get('next'))

def categorize_media(request, figure_id, media_category):
    med = Figure.objects.get(pk=figure_id)
    med.media_category = media_category
    med.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
