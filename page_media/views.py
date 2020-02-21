import time
import logging
import subprocess, os
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import resolve, include, path
from django.views import View

from .forms import MediaForm
from admin_app.choices import *
from admin_app.models import PageMedia, Pages, PageMediaAssociation

# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)

class BasicUploadViewMedia(View):

    def get(self, request, page_id):
        media_list = PageMedia.objects.all()
        return render(self.request, 'page_media/basic_upload/index.html', {'media': media_list})

    def post(self, request):
        form = MediaForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            media = form.save()
            data = {'is_valid': True, 'name': media.file.name, 'url': media.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)

class ProgressBarUploadViewMedia(View):
    def get(self, request, page_id):
        # retrieve list of media for this specific Page
        page = get_object_or_404(Pages, pk=page_id)
        media_list = Pages.objects.get(id=page_id).media.all()
        thisPageID = page.pk
        media_categories = MEDIATYPECHOICES
        context = {
            'thisPageID': thisPageID,
            'media': media_list,
            'page': page,
            'media_categories': media_categories,
        }
        return render(self.request, 'page_media/progress_bar_upload/index.html', context)

    def post(self, request, *args, **kwargs):
        time.sleep(1)  # You don't need this line. This is just to delay the process so you can see the progress bar testing locally.
        form = MediaForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            logger.error("YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY")
            # logger.error(str(request.path))
            logger.error(str(self.request.POST))

            thisOriginPath = self.request.POST["origin_path"]

            logger.error('ORIGIN_PATH: ' + thisOriginPath)

            thisPageID = os.path.basename(os.path.normpath(thisOriginPath))

            # thisProblemID = thisOriginPath.split('/')[-1]

            logger.error('PAGE_ID: ' + thisPageID)

            logger.error('FORM: %s ', form)

            if form.is_valid():
                logger.error('FORM IS VALID')
                logger.error('FORM ERRORS: ')
                media = form.save()
            else:
                logger.error('FORM IS NOT VALID')


            logger.error('AFTER FORM.SAVE FOR MEDIA')

            thisMediaID = media.pk
            logger.error('MEDIA ID: ' + str(thisMediaID))

            Pages.objects.get(id=int(thisPageID)).media.add(int(thisMediaID))
            # return redirect('detail', cat_id=cat_id)
            logger.error('AFTER ADD TO MEDIAS')

            # thisProblemID = FigureAssociations.objects.get()
            data = {'is_valid': True, 'name': media.file.name, 'url': media.file.url, 'newMediaID': thisMediaID}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


class DragAndDropUploadViewMedia(View):
    def get(self, request):
        media_list = PageMedia.objects.all()
        return render(self.request, 'page_media/drag_and_drop_upload/index.html', {'media': media_list})

    def post(self, request):
        form = MediaForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            media = form.save()
            data = {'is_valid': True, 'name': media.file.name, 'url': media.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


def delete_media_for_page(request, page_id):
    for fa in Pages.objects.get(id=page_id).media.all():
        logger.error(fa)
        fa.file.delete()
        fa.delete()

    # for figure in Figure.objects.all():
    #     figure.file.delete()
    #     figure.delete()
    return redirect(request.POST.get('next'))

def delete_media(request, media_id):
    med = PageMedia.objects.get(pk=media_id)
    med.delete()
    # return redirect(request.POST.get('next'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def delete_all_media(request):
    for media in PageMedia.objects.all():
        media.file.delete()
        media.delete()
    return redirect(request.POST.get('next'))

def categorize_media(request, media_id, media_category):
    med = PageMedia.objects.get(pk=media_id)
    med.media_category = media_category
    med.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))