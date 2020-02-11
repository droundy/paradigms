from django.urls import path

from . import views

urlpatterns = [
    #path('', views.HomePageView.as_view(), name='home'),
    path('', views.Home.as_view(), name='home'),
    path('loggedout/',views.Loggedout.as_view(), name='loggedout')
]
