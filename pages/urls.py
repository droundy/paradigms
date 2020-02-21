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
    path('page/<int:pk>/edit', views.editpagebyid, name='page_edit_by_id'),
 
    path('loggedout/',views.Loggedout.as_view(), name='loggedout')
]