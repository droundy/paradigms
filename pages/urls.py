from django.urls import path

from . import views

urlpatterns = [
    #path('', views.HomePageView.as_view(), name='home'),
    # path('', views.Home.as_view(), name='home'),
    path('', views.home, name='home'),
    path('whitepapers/', views.white_papers, name='white_papers'),
    path('about/', views.about, name='about'),
    path('history/', views.history, name='history'),
    # The following will eventually to be turned into app.    
    path('courses/', views.courses, name='courses'),

    path('selfedit/', views.selfedit, name='selfedit'),

    path('loggedout/',views.Loggedout.as_view(), name='loggedout')
]