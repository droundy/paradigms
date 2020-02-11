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
    path('solution/<problem_set_id>/', views.problem_set_details_solution, name='problem_set_details_solution'),
    path('edit/<problem_set_id>/', views.edit_problem_set, name='edit_problem_set'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
