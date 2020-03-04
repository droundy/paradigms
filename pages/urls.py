from django.urls import path

from . import views
from .views import page_render

urlpatterns = [
    # A cool example, but not for use here. 
    # path('<page_slug>/', include([
    #     path('about/', views.about),
    #     path('history/', views.history),
    #     path('courses/', views.courses),
    #     path('whitepapers/', views.white_papers)

    # ])),
    path('', views.homepage_render, name='home'),
    path('whitepapers/', views.wp_list_all, name='wp_list_all'),
    path('whitepapers/activities/', views.wp_list_activitytypes, name='wp_list_activitytypes'),
    path('<slug:pagename>/', views.page_render, name='page_display'),
    path('whitepaper/new/', views.page_new, name='page_new'),
    path('whitepaper/<slug:pagename>/', views.page_render, name='whitepaper_display'),
    path('whitepaper/<slug:pagename>/edit', views.page_edit, name='page_edit'),
    path('<slug:pagename>/title', views.page_title, name='page_title'),
    path('<slug:pagename>/edit', views.page_edit, name='page_edit'),    
    path('page/new', views.page_new, name='page_new'),
    path('page/<int:pk>/edit', views.page_edit_by_id, name='page_edit_by_id'),    
 
    path('loggedout/',views.Loggedout.as_view(), name='loggedout')
]
