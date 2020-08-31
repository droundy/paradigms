from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.urls import path
from studentview import views

urlpatterns = [
    path('', views.home, name='sv_home'),
    path('<slug:number>/<slug:year>/schedule', views.schedule, name='sv_schedule'),
    path('<slug:number>/<slug:year>/', views.schedule, {'view': 'schedule'}, name='sv_schedule'),
    path('<slug:number>/', views.schedule, {'view': 'schedule', 'year': 'latest'}, name='sv_latest'),
    path('<slug:number>/<slug:year>/syllabus', views.schedule, {'view': 'syllabus'}, name='sv_syllabus'),
    path('<slug:number>/<slug:year>/<slug:problemset>-solution.html', views.problem_set, {'view': 'solution'}, name='sv_solution'),
    path('<slug:number>/<slug:year>/<slug:problemset>-solution.pdf', views.problem_set, {'view': 'solution-pdf'}, name='sv_solution_pdf'),
    path('<slug:number>/<slug:year>/<slug:problemset>.html', views.problem_set, {'view': 'html'}, name='sv_problemset'),
    path('<slug:number>/<slug:year>/<slug:problemset>.pdf', views.problem_set, {'view': 'pdf'}, name='sv_problemset_pdf'),

    path('handout/<int:pk>', views.handout, {'view': 'html'}, name='sv_handout'),
    path('handout/<int:pk>.pdf', views.handout, {'view': 'pdf'}, name='sv_handout_pdf'),
    path('solution/<int:pk>', views.handout, {'view': 'solution'}, name='sv_activity_solution'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
