from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from problem_sets import views

urlpatterns = [
    path('', views.list_problem_sets, name='list_problem_sets'),
    path('new/', views.problem_set_add, name='problem_set_add'),
    path('list/', views.list_problem_sets, name='list_problem_sets'),
    path('<problem_set_id>/', views.problem_set_details, name='problem_set_details'),
    path('<problem_set_id>/pdf/', views.problem_set_pdf, name='problem_set_pdf'),
    path('solution/<problem_set_id>/', views.problem_set_details_solution, name='problem_set_details_solution'),
    path('<problem_set_id>/solution/pdf/', views.problem_set_pdf_solution, name='problem_set_pdf_solution'),
    path('edit/<problem_set_id>/', views.edit_problem_set, name='edit_problem_set'),
    # path('edit2/<problem_set_id>/', views.edit_problem_set_2, name='edit_problem_set_2'),
    # path('edit3/<problem_set_id>/', views.edit_problem_set_3, name='edit_problem_set_3'),

    path('associate_problem_to_set/<int:problem_set_id>/<int:problem_id>/', views.associate_problem_to_set, name='associate_problem_to_set'),
    path('unassociate_problem_from_set/<int:problem_set_id>/<int:problem_id>/', views.unassociate_problem_from_set, name='unassociate_problem_from_set'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
