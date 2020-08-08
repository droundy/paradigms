from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.urls import path
from courses import views

urlpatterns = [
    path('list', views.course_list, name='course_list'),
    path('', views.course_list, name='course_list'),
    path('new', views.course_list, name='course_new'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
