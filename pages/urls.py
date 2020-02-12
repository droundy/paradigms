from django.urls import path

from . import views
from .views import renderpage

urlpatterns = [
    # A cool example, but not for use here. 
    # path('<page_slug>/', include([
    #     path('about/', views.about),
    #     path('history/', views.history),
    #     path('courses/', views.courses),
    #     path('whitepapers/', views.white_papers)

    # ])),
    path('', views.renderhomepage, name='home'),
    path('<slug:pagename>/', views.renderpage, name='page_display'),
    path('<slug:pagename>/edit', views.editpage, name='page_edit'),
    
    
    
    # # path('<slug:slug>', renderpage.as_view(), name='page_display'),
    # path('', views.home, name='home'),
    # path('<slug>/', views.renderpage, name='white_papers'),
    # path('<pagename>/edit', views.editpage, name='editpage'),
    # path('about/', views.about, name='about'),
    # path('history/', views.history, name='history'),
    # # The following will eventually to be turned into app.    
    # path('courses/', views.courses, name='courses'),
    # path('editpage/', views.editpage, name='editpage'),
    path('loggedout/',views.Loggedout.as_view(), name='loggedout')
]