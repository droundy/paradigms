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
from pages import views
from pages.views import renderpage

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    path('search/', include('site_directory.urls')),

    
    
    #path('', views.index, name='index'),
    path('problem/',include('public_app.urls')),    

    # Load urls for various apps
    path('sequences/', include('sequences.urls')),
    url(r'^figures/', include(('figures.urls', 'figures'), namespace='figures')),
    path('activities/', include('activities.urls')),
    path('problem_sets/', include('problem_sets.urls')),
    url(r'^activity_media/', include(('activity_media.urls', 'activity_media'), namespace='activity_media')),
    

    
    # User management
    # Need to set up templates for these user login/logout/signup links
    # Add the following to lib/python3.6/site-packages/allauth/templates/account/*.html files
    # {% extends "public_app/base.html" %}
    # <!-- "account/base.html" -->
    path('users/', include('users.urls')),
    path('accounts/', include('allauth.urls')),\
    
    # About, home/index, history, and courses are all contained in the Pages app
    path('', include('pages.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)