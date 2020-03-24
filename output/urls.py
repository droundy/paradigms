from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from output import views

urlpatterns = [
    path('', views.output_home, name='output_home'),
    # path('new/', views.add_client, name='add_client'),
    # path('list/', views.list_clients, name='list_clients'),
    # path('invoice_home/', views.get_invoice, name='get_invoice'),
    # path('<client_id>/', views.client_detail, name='client_detail'),
    # path('edit/<client_id>/', views.edit_client, name='edit_client'),
    # path('work/<client_id>/', views.edit_client_work, name='edit_client_work'),
    # path('rates/<client_id>/', views.edit_client_rates, name='edit_client_rates'),

    # A page to verify layout of problem set and initiate a pdf
    path('problem_set/display/<problem_set_id>/', views.output_problem_set_display, name='output_problem_set_display'),

    path('problem_set/pdf/<problem_set_id>/', views.output_problem_set_pdf, name='output_problem_set_pdf'),

    # path('invoices/<client_id>/', views.list_client_invoices, name='list_client_invoices'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
