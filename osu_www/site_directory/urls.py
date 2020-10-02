from django.urls import path
from public_app import views
from django.conf.urls import url, include
from site_directory import views

urlpatterns = [
    # url(r'^homework/keyword/(?P<searchterm>\w+)/$', views.HomeworkKeywordView, name='homework_keyword'),
    
    path('keyword/<searchterm>', views.HomeworkKeywordView, name='homework_keyword'),

    path('', include('haystack.urls')),
]