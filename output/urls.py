from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from output import views
#from django.conf.urls.defaults import url, patterns
#from wkhtmltopdf.views import PDFTemplateView

urlpatterns = [
    path('', views.output_home, name='output_home'),

    # A page to verify layout of problem set and initiate a pdf
    path('problem_set/display/<problem_set_id>/', views.output_problem_set_display, name='output_problem_set_display'),

	path('problem_set/pdf/<problem_set_id>/', views.output_pdf, name='output_pdf'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
