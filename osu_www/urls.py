"""osu_www URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from public_app import views

urlpatterns = [
    path('', include('pages.urls')),
    #path('', views.index, name='index'),
    path('problem/',include('public_app.urls')),
    path('whitepapers/', views.white_papers, name='white_papers'),
    path('about/', views.about, name='about'),
    path('history/', views.history, name='history'),
    path('courses/', views.courses, name='courses'),

    # path('figures/', include('figures.urls'), name='figures'),

    path('sequences/',include('sequences.urls')),
    url(r'^figures/', include(('figures.urls', 'figures'), namespace='figures')),
    path('activities/',include('activities.urls')),
    path('problem_sets/',include('problem_sets.urls')),

    url(r'^activity_media/', include(('activity_media.urls', 'activity_media'), namespace='activity_media')),

    path('directory/',include('site_directory.urls')),

    # Django Admin
    path('admin/', admin.site.urls),
    # User management
    # Need to set up templates for these user login/logout/signup links
    # Add the following to lib/python3.6/site-packages/allauth/templates/account/*.html files
    # {% extends "public_app/base.html" %}
    # <!-- "account/base.html" -->
    path('users/', include('users.urls')),
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
