from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.urls import path
from courses import views

urlpatterns = [
    path('list', views.course_list, name='course_list'),
    path('', views.course_list, name='course_list'),
    path('new', views.course_list, name='course_new'),
    path('<slug:number>/', views.course_view, name='course_view'),
    path('<slug:number>/syllabus/', views.course_view, {'view': 'syllabus'}, name='course_syllabus'),
    path('<slug:number>/years/', views.course_view, {'view': 'years'}, name='course_years'),
    path('<slug:number>/<slug:year>/', views.course_as_taught, name='course_as_taught'),
    path('<slug:number>/<slug:year>/syllabus/', views.course_as_taught, {'view': 'syllabus'}, name='course_as_taught_syllabus'),
    path('<slug:number>/<slug:year>/schedule/', views.course_as_taught, {'view': 'schedule'}, name='course_as_taught_schedule'),
    path('<slug:number>/<slug:year>/edit/', views.course_as_taught_edit, name='course_as_taught_edit'),
    path('<slug:number>/<slug:year>/hw/<slug:problemset>/', views.problem_set, {'view': 'html'}, name='taught_problemset'),
    path('<slug:number>/<slug:year>/solution/<slug:problemset>/', views.problem_set, {'view': 'solution'}, name='taught_solution'),
    path('<slug:number>/<slug:year>/hw/<slug:problemset>.pdf', views.problem_set, {'view': 'pdf'}, name='taught_problemset_pdf'),
    path('<slug:number>/<slug:year>/solution/<slug:problemset>.pdf', views.problem_set, {'view': 'solution-pdf'}, name='taught_solution_pdf'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
