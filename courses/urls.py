from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.urls import path
from courses import views

urlpatterns = [
    path('list', views.course_list, name='course_list'),
    path('', views.course_list, name='course_list'),
    path('new', views.course_list, name='course_new'),
    path('<slug:number>', views.course_view, name='course_view'),
    path('<slug:number>/syllabus', views.course_view, {'view': 'syllabus'}, name='course_syllabus'),
    path('<slug:number>/years', views.course_view, {'view': 'years'}, name='course_years'),
    path('<slug:number>/<slug:year>', views.course_as_taught, name='course_as_taught'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
